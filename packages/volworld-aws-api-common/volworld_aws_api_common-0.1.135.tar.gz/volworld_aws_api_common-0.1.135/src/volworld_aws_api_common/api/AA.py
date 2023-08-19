from typing import Final
from volworld_common.api.CA import CA


# ====== A: Attribute ======
class AA(CA):

    CheckBox: Final[str] = "chkbx"

    Dialog: Final[str] = "dlg"

    Token: Final[str] = "tk"


AAList = [AA, CA]
