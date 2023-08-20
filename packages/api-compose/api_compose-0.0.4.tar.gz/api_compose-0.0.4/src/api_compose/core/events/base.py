from enum import Enum

from pydantic import ConfigDict, BaseModel as _BaseModel


class EventType(Enum):
    # Registration
    ProcessorRegistration = 'ProcessorRegistration'
    CalculateFieldRegistration = 'CalculatedFieldRegistration'

    # Others
    Action = 'Action'
    CalculateFieldRendering = 'CalculatedFieldRendering'
    CLI = 'Cli'
    Default = 'Default'
    Deserialisation = 'Deserialisation'
    Executor = 'Executor'
    ReadConfiguration = 'ReadConfiguration'
    Scheduler = 'Scheduler'
    SchemaValidator = 'SchemaValidator'
    Session = 'Session'
    TemplatedField = 'TemplatedField'
    TextField = 'TextField'

    def __json__(self):
        return self.value


class BaseData(_BaseModel):
    model_config = ConfigDict(extra="allow")


class BaseEvent(_BaseModel):
    event: EventType
    data: BaseData
