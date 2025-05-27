function likeAction(event, postId) {
    var btnLikeElements = document.querySelectorAll("._" + postId + "_btnLike");
    var likeNumElms = document.querySelectorAll("._" + postId + "_like");
    var liked = btnLikeElements[0].value;
    btnLikeElements.forEach(function(btnLike){
        if( btnLike.value === "false"){
            btnLike.value = "true";
            btnLike.style.backgroundColor = '#0f0';
        }
        else{
            btnLike.value = "false";
            btnLike.style.backgroundColor = '#fff';
        }
    });

    var likeNum;
    if( liked === 'true'){
        likeNumElms.forEach(function(likeElm){
            likeNum = parseInt(likeElm.innerText, 10) - 1;
            likeElm.innerText = likeNum;
        });
    }
    else{
        likeNumElms.forEach(function(likeElm){
            likeNum = parseInt(likeElm.innerText, 10) + 1;
            likeElm.innerText = likeNum;
        });
    }
    
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/postspage/update_likes/${postId}/`, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ like: likeNum}));
}

function insertComment(event, postId){
    var inputCmt = document.getElementById(postId + "_comment_detailPost");
    if (inputCmt){
        var contentCmd = inputCmt.value;
    }
    else{
        inputCmt = document.getElementById(postId + "_comment");
        contentCmd = inputCmt.value;
    }

    if(contentCmd.length === 0){
        alert("Type something for your comment!");
        return;
    }

    inputCmt.value = '';

    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/postspage/insert_comment/${postId}/`, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({comment: contentCmd}));
    alert("Comment success!");

    const cmtNumElms = document.querySelectorAll("._" + postId + "_commentNum");
    cmtNumElms.forEach(function(cmtNum){
        cmtNum.innerText = parseInt(cmtNum.innerText, 10) + 1
    });

    showCmt(postId)
}
function showComment(event, postId){
    showCmt(postId)
}
function showCmt(postId) {
    const cmtElm = document.getElementById("containerComment");
    // console.log("comment showed")
    cmtElm.style.display = "flex";

    $.ajax({
        url: `/postspage/get_comments/${postId}/`,
        method: 'GET',
        success: function(response) {

            var comments = response.comments;
            var containerComment = document.getElementById('allCommentOfPostId');

            containerComment.innerHTML = '';

            comments.forEach(function(comment) {
                var commentHTML = `
                    <div id="comment_${comment.id}" class="d-flex flex-start mt-4">
                        <a href="/profile/${comment.authorId}">
                        <img class="rounded-circle shadow-1-strong me-3"
                        src="${comment.img}" alt="avatar" width="65"
                        height="65" />
                        </a>
                        <div class="flex-grow-1 flex-shrink-1">
                        <div>
                            <div class="d-flex justify-content-between align-items-center">
                            <p class="mb-1">
                                ${comment.name} <span class="small"> <i class="fa-solid fa-clock"></i> ${formatTime(comment.time)}</span>
                            </p>
                            <button onclick="deleleCmt(event, ${comment.id})"><i class="fa-solid fa-xmark"></i> </button>
                            </div>
                            <p class="small mb-0"  style="white-space: pre-line;">${comment.content}</p>
                        </div>
                        </div>
                    </div>
                `;
                containerComment.innerHTML += commentHTML;
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function deleleCmt(event, commentId){ 

    var userChoice = window.confirm("Are you sure you want to delete this comment?");

    if (userChoice) {
    $.ajax({
        url: `/postspage/delete_comment/${commentId}/`,
        type: 'POST',
        data: { 'data_id': commentId },
        success: function(response) {
            var containerComment = document.getElementById('comment_' + commentId);
            if(response.success === true){
                containerComment.remove()
                
                const cmtNumElms = document.querySelectorAll("._" + response.postId + "_commentNum");
                cmtNumElms.forEach(function(cmtNum){
                    cmtNum.innerText = parseInt(cmtNum.innerText, 10) - 1
                });
                alert("Comment deleted!")
            }
            else{
                alert("You cannot delete other people's comments!")
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
    }
}

function formatTime(timeString) {

    const date = timeString.substring(0, timeString.indexOf('T'));
    const time = timeString.substring(timeString.indexOf('T') + 1, timeString.indexOf('T') + 6);
    //const formattedTime = `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
    const formattedTime = `${date} ${time}`;
    return formattedTime;
}


function search_post(event){
    var searchElement = document.getElementById("searchPosts");
    var searchKey = searchElement.value;
    $.ajax({
        url: `/postspage/search/`,
        type: 'POST',
        data: {'searchKey': searchKey},
        success: function(response) {
            var resultSearchElement = document.getElementById("resultPostSearch");
            resultSearchElement.innerHTML = '';

            dataSearch = response.dataSearch;
            dataSearch.forEach(function (post){
                var resultElement1 = `
                    <div class="result">
                        <a href="/profile/${post.authorId}">
                            <img src="${post.avatar}" alt="User 1" class="avatar">
                        </a>
                        <div class="info">
                            <h5><strong>${post.name}</strong></h5>
                            <p>Tiêu đề:
                                <strong class="titleLink" onclick = "showDetailPosts(event, ${post.id} )">${post.title}</strong>
                            </p>
                            <div class="groupInResult">
                                <i class="fa-solid fa-location-dot"></i>
                `;

                var address;
                if( post.provider){
                    address = `
                                <a href="/profile/${post.provider.id}"><p>${post.provider.name}</p></a>
                    `;
                }
                else{
                    address = `
                                <p>${post.address}</p>
                    `;
                }
                var resultElement2 = `
                            </div>
                            <div class="groupInResult">
                                <i class="fa-solid fa-thumbs-up"> ${post.like} </i>
                                <i class="fa-solid fa-comment"> ${post.cmt} </i>
                            </div>
                        </div>
                    </div>
                `;
                resultSearchElement.innerHTML += (resultElement1 + address + resultElement2);

            })
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function showDetailPosts(event, postId ){
    $.ajax({
        url: `/postspage/search/detail/${postId}/`,
        type: 'POST',
        success: function(response) {
            var containerPost = document.getElementById("containerPost");
            containerPost.style.display = 'flex';
            var showADetailPost = document.getElementById("showADetailPost");

            detailPost = response.detailPost;
            var div1 = `
                <div class="info">
                    <a href="">
                        <img src="${detailPost.authorAvatar}" alt="" class="avatar">
                    </a>
                    <h3><strong>${detailPost.authorName}</strong></h3>
                    <h6>Time: <strong> ${formatTime(detailPost.time)}</strong></h6>
                    <p>
                    Đang ở: <a href=""><strong>${detailPost.provider}</strong></a>
                    </p>
                </div>
                <h3><strong>${detailPost.title}</strong></h3>
                <p  style="white-space: pre-line;">${detailPost.content}</p>
                <div class="post-photo">
            `;
            // vòng for hiển thị các ảnh
            detailPost.img.forEach(function(img){
                div1 += `
                <img src="${img}" alt="Post 1" class="photo">
                `;
            });

            div1 += `
                </div>

                <div class="post-actions">
            `;
            
            if(detailPost.userLike){
                div1 += `<button class="_${postId}_btnLike" value="true" onclick="likeAction(event, ${postId})" style="background-color: #0f0;">`; 
            }
            else{
                div1 += `<button class="_${postId}_btnLike" value="false" onclick="likeAction(event, ${postId})"> `;
            }

            div1 += `
                        <big class="_${postId}_like">${detailPost.like}</big> 
                        <i class="far fa-thumbs-up"></i>
                    </button>
                    <!-- Comment -->
                    <button onclick="showComment(event, ${postId})"> 
                        <big class="_${postId}_commentNum">${detailPost.cmt} </big> 
                        <i class="far fa-comment"></i> 
                    </button>
                </div>

                <div class="post-comment">
                    <img src="${detailPost.user.avatar}" alt="" class="avatar">
                    <input type="text" placeholder="Comment something ..." class="comment" id="${postId}_comment_detailPost">
                    <button class="sendCmt" onclick="insertComment(event, ${postId})">Send</button>
                </div>
            `;
            showADetailPost.innerHTML = div1;
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function cancelDetailPost(){
    var containerComment = document.getElementById('containerPost');
    containerComment.style.display = 'none';
}