from . import models
from . import wizards


# post_init_hook gom (fold) cac stage maintenance goc de Kanban 0502 chi noi bat cac cot 0502
# khong xoa stage goc (chi fold) de tranh anh huong du lieu maintenance dang dung
def post_init_hook(env):
    base_stage_xmlids = (
        "maintenance.stage_0",
        "maintenance.stage_1",
        "maintenance.stage_3",
        "maintenance.stage_4",
    )
    for xmlid in base_stage_xmlids:
        stage = env.ref(xmlid, raise_if_not_found=False)
        if stage and not stage.fold:
            stage.fold = True

# khai báo một thư mục là module hay package, nó sẽ tự động tìm kiếm file __init__.py để thực thi, nếu không có file này thì thư mục đó sẽ không được coi là một module hay package.
