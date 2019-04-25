function apiRequest(request, callback) {
  /**
   * Handle api requests.
   * Allows two inputs, request and callback.
   * If request is valid, then pass and evaluate callback.
   */
  return $.ajax({
    method: "POST",
    url: "/api/v1/http",
    contentType: "application/json",
    data: JSON.stringify(request),
    // Parse the returned response into JSON.
    dataType: "json",
    success: callback,
    // TODO: better error handling.
    error: console.error
  });
}

function decodeHash(hash) {
  /**
   * Decode hash
   */
  const result = {};
  for (let component of decodeURI(hash).split(",")) {
    let [key, value] = component.split(":");
    if (value === undefined) {
      continue;
    }
    result[key] = value;
  }
  return result;
}

function encodeHash(hash) {
  /**
   * Encode hash
   */
  return encodeURI(
    Object.entries(hash)
      .map(mapping => mapping.join(":"))
      .join(",")
  );
}

//Below handles clicks on screen, hasing the location
$(".homeLink").each((index, value) => {
  $(value).on("click", () => {
    window.location.href = "/" + window.location.hash;
  });
});
