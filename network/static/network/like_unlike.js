function like_post(id, likedby) {
    fetch(`/postapi/${id}`)
        .then(response => response.json())
        .then(blogpost => {
            const likescount = blogpost.likes
            fetch(`/likesapi/${id}`, {
                method: 'POST',
                body: JSON.stringify({
                    "id": id,
                    "likedby": likedby[0],
                    "likes": likescount + 1
                })
            })
                .then(response => response.json())
                .then(result => {
                    likesdiv = document.querySelector(`#likes-${id}`)
                    likesdiv.innerHTML = `<div class="unlikebtn">
                        <img id="unlikebtn-${id}" 
                        src="/static/network/heart-fill.svg" alt="" width="15" height="15" />&nbsp;${likescount + 1}
                    </div>`
                    unlikebtn = document.querySelector(`#unlikebtn-${id}`)
                    unlikebtn.onclick = () => {
                        unlike_post(id, likedby)
                    }
                });
        });
}

function unlike_post(id, unlikedby) {
    fetch(`/postapi/${id}`)
        .then(response => response.json())
        .then(bpost => {
            const likescount = bpost.likes
            fetch(`/likesapi/${id}`, {
                method: 'DELETE',
                body: JSON.stringify({
                    "id": id,
                    "unlikedby": unlikedby[0],
                    "likes": likescount - 1
                })
            })
                .then(response => response.json())
                .then(result => {
                    likesdiv = document.querySelector(`#likes-${id}`)
                    likesdiv.innerHTML = `<div class="likebtn">
                        <img id="likebtn-${id}" 
                        src="/static/network/heart.svg" alt="" width="15" height="15" />&nbsp;${likescount - 1}
                    </div>`
                    likebtn = document.querySelector(`#likebtn-${id}`)
                    likebtn.onclick = () => {
                        like_post(id, unlikedby)
                    }
                });
        });
}