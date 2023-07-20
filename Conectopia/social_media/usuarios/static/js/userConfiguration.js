function valitePassword(userPassword)

    oldPassword = document.getElementById("txtOldPassword").value
    newPassword = document.getElementById("txtNewPassword").value
    passwordConfirmation = document.getElementById("txtPasswordConfirmation").value

    if (oldPassword != newPassword) {
        document.getElementById('txtError').innerHTML = 'The password does not match with your old password'
        document.getElementById('saveDiv').style.display = 'none'
    }

