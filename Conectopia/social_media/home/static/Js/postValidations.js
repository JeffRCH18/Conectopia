function editPost(postID, postTxt, postType) {

    var myModal = document.getElementById('updatePostModal');
    document.getElementById('txtIdPost').value = postID
    document.getElementById('txtUpdatePost').value = postTxt


    const imagePath = "/static/shared_images/post_" + postID + ".png";


    document.getElementById('postUpdateImage').src = imagePath
    


    document.getElementById('txtUpdatePostPreference').value = postType
    document.getElementById('txtUpdatePostImage').value = ''
    $(myModal).modal('show')


}

function deletePost(postID) {

    var myModal = document.getElementById('deletePostModal');
    document.getElementById('txtIdPost').value = postID
    $(myModal).modal('show')


}