
class ProjectNotFoundError(Exception):
    pass

class ProjectAccessDeniedError(Exception):
    pass


class TaskNotFoundError(Exception):
    pass

class TaskAccessDeniedError(Exception):
    pass

class TaskIsEmpty(Exception):
    pass