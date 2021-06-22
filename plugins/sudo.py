# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
📚 Commands Available -

• `{i}addsudo`
    Add Sudo Users by replying to user or using <space> separated userid(s)

• `{i}delsudo`
    Remove Sudo Users by replying to user or using <space> separated userid(s)

• `{i}listsudo`
    List all sudo users.
"""

from pyUltroid.misc import sudoers

from . import *


@ultroid_cmd(
    pattern="addsudo ?(.*)",
)
async def _(ult):
    if not ult.out and not is_fullsudo(ult.sender_id):
        return await eod(ult, "`perintah ini dibatasi untuk anggota sudo!..`")
    inputs = ult.pattern_match.group(1)
    if str(ult.sender_id) in sudoers():
        return await eod(ult, "`anggota sudo tidak dapat menambahkan anggota sudo baru!`", time=10)
    ok = await eor(ult, "`memperbarui daftar anggota sudo...`")
    mmm = ""
    if ult.reply_to_msg_id:
        replied_to = await ult.get_reply_message()
        id = await get_user_id(replied_to.sender_id)
        name = (await ult.client.get_entity(int(id))).first_name
        if id == ultroid_bot.me.id:
            mmm += "kamu tidak dapat menambahkan dirimu sendiri sebagai anggota sudo..."
        elif is_sudo(id):
            mmm += f"[{name}](tg://user?id={id}) `sudah menjadi anggota sudo...`"
        elif add_sudo(id):
            udB.set("SUDO", "True")
            mmm += f"**menambahkan [{name}](tg://user?id={id}) sebagai anggota sudo.**"
        else:
            mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
    elif inputs:
        id = await get_user_id(inputs)
        try:
            name = (await ult.client.get_entity(int(id))).first_name
        except BaseException:
            name = ""
        if id == ultroid_bot.me.id:
            mmm += "kamu tidak dapat menambahkan dirimu sendiri sebagai anggota sudo..."
        elif is_sudo(id):
            if name != "":
                mmm += f"[{name}](tg://user?id={id}) `sudah menjadi anggota sudo...`"
            else:
                mmm += f"`{id} sudah menjadi anggota sudo...`"
        elif add_sudo(id):
            udB.set("SUDO", "True")
            if name != "":
                mmm += f"**menambahkan [{name}](tg://user?id={id}) sebagai anggota sudo**"
            else:
                mmm += f"**menambahkan **`{id}`** sebagai anggota sudo**"
        else:
            mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
    else:
        mmm += "`balas ke pesan nya atau tambahkan melalui id/username nya.`"
    await eod(ok, mmm)


@ultroid_cmd(
    pattern="delsudo ?(.*)",
)
async def _(ult):
    if not ult.out and not is_fullsudo(ult.sender_id):
        return await eod(ult, "`perintah ini dibatasi untuk anggota sudo!`")
    inputs = ult.pattern_match.group(1)
    if str(ult.sender_id) in sudoers():
        return await eod(
            ult,
            "kamu anggota sudo, tidak dapat menghapus anggota sudo lain.",
        )
    ok = await eor(ult, "`memperbarui daftar anggota sudo...`")
    mmm = ""
    if ult.reply_to_msg_id:
        replied_to = await ult.get_reply_message()
        id = await get_user_id(replied_to.sender_id)
        name = (await ult.client.get_entity(int(id))).first_name
        if not is_sudo(id):
            mmm += f"[{name}](tg://user?id={id}) `bukan anggota sudo...`"
        elif del_sudo(id):
            mmm += f"**menghapus [{name}](tg://user?id={id}) dari anggota sudo.(s)**"
        else:
            mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
    elif inputs:
        id = await get_user_id(inputs)
        try:
            name = (await ult.client.get_entity(int(id))).first_name
        except BaseException:
            name = ""
        if not is_sudo(id):
            if name != "":
                mmm += f"[{name}](tg://user?id={id}) `bukan anggota sudo...`"
            else:
                mmm += f"`{id} bukan anggota sudo...`"
        elif del_sudo(id):
            if name != "":
                mmm += f"**menghapus [{name}](tg://user?id={id}) dari anggota sudo.(s)**"
            else:
                mmm += f"**menghapus **`{id}`** dari anggota sudo.(s)**"
        else:
            mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
    else:
        mmm += "`Reply to a msg or add it's id/username.`"
    await eod(ok, mmm)


@ultroid_cmd(
    pattern="listsudo$",
)
async def _(ult):
    ok = await eor(ult, "`...`")
    sudos = Redis("SUDOS")
    if sudos == "" or sudos is None:
        return await eod(ult, "`No SUDO User was assigned ...`", time=5)
    sumos = sudos.split(" ")
    msg = ""
    for i in sumos:
        try:
            name = (await ult.client.get_entity(int(i))).first_name
        except BaseException:
            name = ""
        if name != "":
            msg += f"• [{name}](tg://user?id={i}) ( `{i}` )\n"
        else:
            msg += f"• `{i}` -> Invalid User\n"
    m = udB.get("SUDO") if udB.get("SUDO") else "False"
    if m == "False":
        m = "[False](https://telegra.ph/Ultroid-04-06)"
    return await ok.edit(
        f"**SUDO MODE : {m}\n\n🌸 daftar anggota sudo :**\n{msg}", link_preview=False
    )
