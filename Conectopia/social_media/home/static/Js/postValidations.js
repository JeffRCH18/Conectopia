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
            document.getElementById('txtpostComment').value = ""
            document.getElementById('txtIdPostComment').value = postID
            $(myModal).modal('show')

        },
        error: function (error) {
            console.log('Error:', error);
        }
    });

}

//Create a new comment
function createNewComment() {

    postID = document.getElementById('txtIdPostComment').value
    comment = document.getElementById('txtpostComment').value

    $.ajax({
        url: '/create_comment/',
        type: 'GET',
        data: { postID: postID,comment:comment},
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
                document.getElementById('txtpostComment').value = ""

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

function getLikePost(postID) {

    $.ajax({
        url: '/get_likes/',
        type: 'GET',
        data: { postID: postID },
        dataType: 'json',
        success: function (data) {

            //print_data
            console.log(data)

            //Change the liked button depending if the user already liked or not.
            if (data.user_liked == true) {
                document.getElementById('likeForm').style.display = 'none'
                document.getElementById('dislikeForm').style.display = ''
            } else {
                document.getElementById('likeForm').style.display = ''
                document.getElementById('dislikeForm').style.display = 'none'
            }

            var commentsLists = $('#likesList');
            commentsLists.empty();
            likesData = data.likes

            for (var i = 0; i < likesData.length; i++) {
                var like = likesData[i];
                var userName = like.userName;
                var picPath = '/static/' + like.picPath;

                // Create the elements for each like using jQuery
                var rowDiv = $('<div>').addClass('row justify-content-center').css('margin-top', '15px');

                var colDiv = $('<div>').addClass('col-md-11');

                var cardDiv = $('<div>').addClass('card').css({
                    'background-color': 'rgba(177, 156, 217, 0.432)',
                    'border': 'none'
                });

                var cardBodyDiv = $('<div>').addClass('card-body');

                var innerRowDiv = $('<div>').addClass('row');

                var profilePicDiv = $('<div>').addClass('col-md-2');

                var profilePicImg = $('<img>').attr({
                    'src': picPath,
                    'alt': 'profilepic'
                }).addClass('rounded-circle img-fluid bg-white').css({
                    'object-fit': 'cover',
                    'width': '60%',
                    'height': '55px'
                });

                var userInfoDiv = $('<div>').addClass('col-md-10');

                var userNameParagraph = $('<p>').addClass('text-muted').css('margin', '3px').text(userName);

                var likeParagraph = $('<p>').text('Likes this post').css('margin-bottom', '0px');

                // Append the elements to each other
                profilePicDiv.append(profilePicImg);

                userInfoDiv.append(userNameParagraph);
                userInfoDiv.append(likeParagraph);

                innerRowDiv.append(profilePicDiv);
                innerRowDiv.append(userInfoDiv);

                cardBodyDiv.append(innerRowDiv);

                cardDiv.append(cardBodyDiv);

                colDiv.append(cardDiv);

                rowDiv.append(colDiv);

                // Append the newly created rowDiv to the commentsLists div using jQuery
                commentsLists.append(rowDiv);
            }

            //Modify the require information in the form to create a new comment and show the modal
            var myModal = document.getElementById('postLikesModal');
            document.getElementById('txtIdpostLikes').value = postID
            document.getElementById('txtIdpostDislike').value = postID
            $(myModal).modal('show')



        },
        error: function (error) {
            console.log('Error:', error);
        }
    });
}

function LikePost() {

    postID = document.getElementById('txtIdpostLikes').value

    $.ajax({
        url: '/postLikes/',
        type: 'GET',
        data: { postID: postID},
        dataType: 'json',
        success: function (data) {

            //print_data
            console.log(data)

            //Change the liked button depending if the user already liked or not.
            if (data.user_liked == true) {
                document.getElementById('likeForm').style.display = 'none'
                document.getElementById('dislikeForm').style.display = ''
            } else {
                document.getElementById('likeForm').style.display = ''
                document.getElementById('dislikeForm').style.display = 'none'
            }

            var commentsLists = $('#likesList');
            commentsLists.empty();
            likesData = data.likes

            for (var i = 0; i < likesData.length; i++) {
                var like = likesData[i];
                var userName = like.userName;
                var picPath = '/static/' + like.picPath;

                // Create the elements for each like using jQuery
                var rowDiv = $('<div>').addClass('row justify-content-center').css('margin-top', '15px');

                var colDiv = $('<div>').addClass('col-md-11');

                var cardDiv = $('<div>').addClass('card').css({
                    'background-color': 'rgba(177, 156, 217, 0.432)',
                    'border': 'none'
                });

                var cardBodyDiv = $('<div>').addClass('card-body');

                var innerRowDiv = $('<div>').addClass('row');

                var profilePicDiv = $('<div>').addClass('col-md-2');

                var profilePicImg = $('<img>').attr({
                    'src': picPath,
                    'alt': 'profilepic'
                }).addClass('rounded-circle img-fluid bg-white').css({
                    'object-fit': 'cover',
                    'width': '60%',
                    'height': '55px'
                });

                var userInfoDiv = $('<div>').addClass('col-md-10');

                var userNameParagraph = $('<p>').addClass('text-muted').css('margin', '3px').text(userName);

                var likeParagraph = $('<p>').text('Likes this post').css('margin-bottom', '0px');

                // Append the elements to each other
                profilePicDiv.append(profilePicImg);

                userInfoDiv.append(userNameParagraph);
                userInfoDiv.append(likeParagraph);

                innerRowDiv.append(profilePicDiv);
                innerRowDiv.append(userInfoDiv);

                cardBodyDiv.append(innerRowDiv);

                cardDiv.append(cardBodyDiv);

                colDiv.append(cardDiv);

                rowDiv.append(colDiv);

                // Append the newly created rowDiv to the commentsLists div using jQuery
                commentsLists.append(rowDiv);
            }

            //Modify the require information in the form to create a new comment and show the modal
            var myModal = document.getElementById('postLikesModal');
            document.getElementById('txtIdpostLikes').value = postID
            document.getElementById('txtIdpostDislike').value = postID
            $(myModal).modal('show')



        },
        error: function (error) {
            console.log('Error:', error);
        }
    });
}