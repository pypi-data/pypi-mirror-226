import logging
from argparse import ArgumentParser
from wesync.services.interaction.userInteraction import UserInteraction
from wesync.services.projectManagerFactory import ProjectManagerFactory
from wesync.services.snapshot import SnapshotManager, Snapshot
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.execute.RsyncFileTransferService import RsyncFileTransfer
from wesync.services.processors.processorManager import ProcessorManager


class SnapshotImportOperation(Operation):

    operationName = 'import'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config
        self.processorManager = ProcessorManager(self.config)

        self.userInteraction = UserInteraction()

        self.deployment = self.config.getDeployment()
        self.deployment.ensureKeysAreSet(["name", "path"])

        self.project = self.deployment.getProject()
        self.project.ensureKeysAreSet(['name', 'type'])

        self.projectManager = ProjectManagerFactory.getProjectManagerFor(self.deployment, self.config)
        self.snapshotManager = SnapshotManager(self.config)

    def run(self):
        snapshot = self.snapshotManager.getActiveSnapshotFor(self.project.getName())
        if not snapshot:
            logging.error("Snapshot label or path must be specified")

        if self.deployment.isProtected():
            if self.userInteraction.confirm("Target deployment is protected. Continue ?", level='warn') is False:
                return False

        if self.deployment.isLocal():
            self.projectManager.fullImport(snapshot)
        else:
            filetransfer = RsyncFileTransfer(self.config)

            projectName = self.project.getName()
            tmpDirName = '/var/tmp/westash/' + projectName
            self.projectManager.createPath(tmpDirName)

            remoteSnapshot = Snapshot(tmpDirName)
            logging.info("Copying snapshot to remote deployment")
            filetransfer.copyToRemote(
                snapshot.getPath() + "/",
                self.deployment,
                destinationPath=tmpDirName
            )

            self.projectManager.fullImport(remoteSnapshot)
            self.projectManager.deletePath(tmpDirName, recursive=True)

        if self.config.get('delete') is True:
            snapshot.delete()

        importProcessors = self.processorManager.getForAnyTrigger(['import'], self.deployment)
        importProcessors.executeAll()

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--delete", help="Delete snapshot after import", action='store_true')
        argumentParser.add_argument("--path", help="Import according to path")
        argumentParser.add_argument("label", help="Label of the import", nargs='?')
        return argumentParser

