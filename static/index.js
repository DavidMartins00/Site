function deleteUser(userId){
    fetch('/delete-user',{
        method: 'POST',
        body: JSON.stringify({userId: userId}),
    }).then((_res) => {
        window.location.href = "/users";
    });
}

function editUser(userId){
    fetch('/edit-user',{
        method: 'POST',
        body: JSON.stringify({userId: userId}),
    }).then((_res) => {
        //window.location.href = "/users";
    });
}
