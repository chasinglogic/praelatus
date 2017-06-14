var converter = new showdown.Converter();

function reloadPreview(ele) {
    let value = ele.value;
    let pc = document.getElementById(ele.id + '-preview-content');
    pc.innerHTML = converter.makeHtml(value);
}

function deleteComment(ele) {
    if (!confirm('Are you sure you want to delete this comment?')) {
        return;
    }

    let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0];
    fetch('/tickets/comments/' + ele.id, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken.value
        },
        credentials: 'same-origin'
    }).
        then(function(res) {
            if(res.ok) {
                window.location.reload(true);
            } else {
                alert('Error!');
                console.log(res);
                console.log(res.text().then(console.log));
            }
        });
}


// Store the original content of a comment card.
var originals = {}

function editComment(ele) {
    let formHTML = document.getElementById('edit-form-container').innerHTML;
    let card = document.getElementById('comment-' + ele.id);
    let body = document.getElementById('comment-' + ele.id + '-body');

    originals['comment-' + ele.id] = card.innerHTML;
    card.innerHTML = formHTML;

    let ta = document.getElementById('edit-comment');
    ta.value = body.innerText;

    let form = document.getElementById('edit-comment-comment-form');
    form.action = '/tickets/comments/' + ele.id;

    let next = document.getElementById('edit-comment-next');
    next.value = next.value + '#comment-' + ele.id;

    reloadPreview(ta);
}


function getCommentId(el) {
    if (el.id.startsWith('comment-')) {
        return el.id;
    }

    return getCommentId(el.parentElement);
}

function cancelEdit(ele) {
    let commentId = getCommentId(ele);
    console.log('commentId', commentId);

    let card = document.getElementById(commentId)
    card.innerHTML = originals[commentId];
}
