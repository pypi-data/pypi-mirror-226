from typing import Final
from volworld_common.api.CA import CA


# ====== A: Attribute ======
class AA(CA):
    AppBar: Final[str] = "ab"

    BottomAppBar: Final[str] = "btmab"

    CheckBox: Final[str] = "chkbx"

    Dialog: Final[str] = "dlg"

    NextPage: Final[str] = "nxp"

    PreviousPage: Final[str] = "prp"

    Switch: Final[str] = "sth"

    Token: Final[str] = "tk"


AAList = [AA, CA]
