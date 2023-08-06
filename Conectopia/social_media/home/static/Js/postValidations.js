//Prepare the edit form to do edits to a post
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

//Prepare the delete form to delete a post
function deletePost(postID) {

    var myModal = document.getElementById('deletePostModal');
    document.getElementById('txtIdDeletePost').value = postID
    $(myModal).modal('show')


}

//Do a call to the server and bring all the comments related to a line, in addition bring the list of comments.
function commentPost(postID) {

    $.ajax({
        url: '/get_comentarios/',
        type: 'GET',
        data: { postID: postID },
        dataType: 'json',
        success: function (data) {

            // Get the reference to the commentsList div
            var commentsListDiv = $('#commentsList');

            // Clear the commentsList div before appending new elements (optional)
            commentsListDiv.empty();


            //Create the list of users
            for (var i = 0; i < data.length; i++) {

                var comentario = data[i].comentario;
                var usuario = data[i].usuario;
                var nombreUsuario = usuario.nombre;
                var imagenUsuario = '/static/' + usuario.imagen;

                // Create the HTML elements for the comment
                var rowDiv = $('<div>').addClass('row justify-content-center').css('margin-top', '15px');
                var colDiv = $('<div>').addClass('col-md-11');
                var cardDiv = $('<div>').addClass('card').css({
                    'background-color': 'rgba(177, 156, 217, 0.432)',
                    'border': 'none'
                });
                var cardBodyDiv = $('<div>').addClass('card-body');
                var rowInnerDiv = $('<div>').addClass('row');
                var colUserDiv = $('<div>').addClass('col-md-2');
                var profilePicImg = $('<img>').attr({
                    'src': imagenUsuario,
                    'alt': 'profilepic'
                }).addClass('rounded-circle img-fluid bg-white').css({
                    'object-fit': 'cover',
                    'width': '80%',
                    'height': '75px'
                });
                var colTextDiv = $('<div>').addClass('col-md-10');
                var userNameP = $('<p>').addClass('text-muted').text(nombreUsuario);
                var commentTextP = $('<p>').text(comentario);

                // Append the elements to their parent elements
                colUserDiv.append(profilePicImg);
                colTextDiv.append(userNameP, commentTextP);
                rowInnerDiv.append(colUserDiv, colTextDiv);
                cardBodyDiv.append(rowInnerDiv);
                cardDiv.append(cardBodyDiv);
                colDiv.append(cardDiv);
                rowDiv.append(colDiv);

                // Append the comment HTML elements to the commentsList div
                commentsListDiv.append(rowDiv);

            }

            //Modify the require information in the form to create a new comment and show the modal
            var myModal = document.getElementById('postCommentModal');
            document.getElementById('txtIdPostComment').value = postID
            $(myModal).modal('show')

        },
        error: function (error) {
            console.log('Error:', error);
        }
    });

}