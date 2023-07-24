function valitePassword(userPassword) {

    oldPassword = document.getElementById("txtOldPassword").value
    newPassword = document.getElementById("txtNewPassword").value
    passwordConfirmation = document.getElementById("txtPasswordConfirmation").value

    //Validate old password user
    if (oldPassword != userPassword) {
        document.getElementById('errorAlert').style.display = ''
        document.getElementById('txtError').innerHTML = 'The password does not match with your old password'
        document.getElementById('saveDiv').style.display = 'none'
        //Validate the password confirmation
    } else if (newPassword != passwordConfirmation) {
        document.getElementById('errorAlert').style.display = ''
        document.getElementById('txtError').innerHTML = 'The password confirmation does not match with the original password'
        document.getElementById('saveDiv').style.display = 'none'
        //Hide the error and show the button.
    } else if ((newPassword.length == 0) || (passwordConfirmation.length == 0)) {
        document.getElementById('errorAlert').style.display = ''
        document.getElementById('txtError').innerHTML = 'Please complete all the information'
        document.getElementById('saveDiv').style.display = 'none'
    } else {
        document.getElementById('errorAlert').style.display = 'none'
        document.getElementById('saveDiv').style.display = ''
    }


}
