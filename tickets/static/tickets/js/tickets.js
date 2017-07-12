var converter = new showdown.Converter();

function reloadPreview(ele) {
    var value = ele.value;
    var pc = document.getElementById(ele.id + '-preview-content');
    pc.innerHTML = converter.makeHtml(value);
}

function devareComment(ele) {
    if (!confirm('Are you sure you want to devare this comment?')) {
        return;
    }

    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0];
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
var originals = {};

function editComment(ele) {
    var formHTML = document.getElementById('edit-form-container').innerHTML;
    var card = document.getElementById('comment-' + ele.id);
    var body = document.getElementById('comment-' + ele.id + '-body');

    originals['comment-' + ele.id] = card.innerHTML;
    card.innerHTML = formHTML;

    var ta = document.getElementById('edit-comment');
    ta.value = body.innerText;

    var form = document.getElementById('edit-comment-comment-form');
    form.action = '/tickets/comments/' + ele.id;

    var next = document.getElementById('edit-comment-next');
    next.value = next.value + '#comment-' + ele.id;

    reloadPreview(ta);
}


function getCommentId(el) {
    if (el.id.startsWith('comment-') && el.id != 'comment-form') {
        return el.id;
    }

    return getCommentId(el.parentElement);
}

function cancelEdit(ele) {
    var commentId = getCommentId(ele);
    console.log('commentId', commentId);

    var card = document.getElementById(commentId);
    card.innerHTML = originals[commentId];
}
