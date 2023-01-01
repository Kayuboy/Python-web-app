function deleteUser(id) {
  fetch(`/delete/${id}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      location.reload();
    })
    .catch((error) => {
      console.error(error);
    });
}
