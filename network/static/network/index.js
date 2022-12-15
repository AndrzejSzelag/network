function edit_post(id) {
    fetch(`/postapi/${id}`)
        .then(response => response.json())
        .then(blogpost => {
            cardbody = document.querySelector(`#card-body-${id}`);
            cardbody.innerHTML = `<form id="editform-${blogpost.id}">
            <div class="form-group my-1">
            <small class="form-text text-muted"><strong>Required</strong>, maximum 300 characters</small>
            <textarea class="form-control" id="textarea-${blogpost.id}" rows="3" name="content" maxlength="300" required>${blogpost.content}</textarea>
            <button class="mt-1 btn btn-sm btn-light border" type="submit" value="Save">
            <span class="spinner-grow spinner-grow-sm text-warning" role="status" aria-hidden="true"></span>
            Save</button></form>`;
            const form = document.querySelector(`#editform-${blogpost.id}`);
            form.onsubmit = () => {
                const textarea = document.querySelector(`#textarea-${blogpost.id}`).value;
                fetch(`/postapi/${blogpost.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: textarea,
                        username: blogpost.username
                    })
                })
                show_content(`${blogpost.id}`);
                return false;
            }
        });
}

function show_content(id) {
    fetch(`/postapi/${id}`)
        .then(response => response.json())
        .then(blogpost => {
            cardbody.innerHTML = `<div class="p-1 card-text">
                                <span class="text-dark my_font_content">${blogpost.content}</span>
                                </div>`;
        });
}