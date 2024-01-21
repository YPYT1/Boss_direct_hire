from myApp.models import User
import hashlib
def changePassword(passwordInfo,userInfo):
    oldPwd = passwordInfo['oldPassword']
    newPwd = passwordInfo['newPassword']
    newCheckPwd = passwordInfo['newCheckPassword']
    user = User.objects.get(username=userInfo.username)
    md5 = hashlib.md5()
    md5.update(oldPwd.encode())
    oldPwd = md5.hexdigest()

    if user.password != oldPwd:
        return '原始密码不正确'
    else:
        if newPwd != newCheckPwd:
            return '新密码两次不符合'
        else:
            md5 = hashlib.md5()
            md5.update(newPwd.encode())
            newPwd = md5.hexdigest()
            user.password = newPwd
            user.save()
