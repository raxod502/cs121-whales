function apiRequest(request, callback) {
  $.ajax({
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
  return encodeURI(
    Object.entries(hash)
      .map(mapping => mapping.join(":"))
      .join(",")
  );
}
