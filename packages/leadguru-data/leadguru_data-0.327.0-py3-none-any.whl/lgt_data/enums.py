from enum import Enum, IntFlag


class DedicatedBotState(IntFlag):
    Operational = 0
    Stopped = 1
    ScheduledForDeletion = 2


class UserAccountState(IntFlag):
    Operational = 0
    Suspended = 1


class UserRole(str, Enum):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'


class BotType(str, Enum):
    DEDICATED_BOT = 'dedicated',
    USER_BOT = 'user',
    LEADGURU_BOT = 'leadguru'


class GoogleCloudFolder(str, Enum):
    SLACK_PROFILE_FILES = "Slack_profile"
    TICKET_FILES = "Ticket"


class SourceType(str, Enum):
    SLACK = 'slack'
    Discord = 'discord'


class BotUpdateEventType(str, Enum):
    NotDefined = 'NotDefined'
    BotAdded = 'BotAdded'
    BotDeleted = 'BotDeleted'
    BotUpdated = 'BotUpdated'


class UserAction(str, Enum):
    PAUSE_CHANNEL = 'monitoring.pause.channel'
    PAUSE_WORKSPACE = 'monitoring.pause.workspace'
    PAUSE_SOURCE = 'monitoring.pause.source'
    UNPAUSE_CHANNEL = 'monitoring.unpause.channel'
    UNPAUSE_WORKSPACE = 'monitoring.unpause.workspace'
    UNPAUSE_SOURCE = 'monitoring.unpause.source'
    STOP_CHANNEL = 'monitoring.stop.channel'
    STOP_WORKSPACE = 'monitoring.stop.workspace'
    STOP_SOURCE = 'monitoring.stop.source'
    START_CHANNEL = 'monitoring.start.channel'
    START_WORKSPACE = 'monitoring.start.workspace'
    START_SOURCE = 'monitoring.start.source'
    LOGIN = 'login'
    LEAD_SAVE = 'lead.save'


class StatusConnection(str, Enum):
    IN_PROGRESS = 'In progress',
    COMPLETE = 'Complete',
    FAILED = 'Failed'


class DefaultBoards(str, Enum):
    Inbox = 'Inbox',
    Primary = 'Primary board'
