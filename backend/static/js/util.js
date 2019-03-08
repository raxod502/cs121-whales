const apiRequest = function(request, callback) {
  $.ajax({
    method: "POST",
    url: "/api/v1/http",
    contentType: "application/json",
    data: JSON.stringify(request),
    // Parse the returned response into JSON.
    dataType: "json",
    success: callback,
    error: console.error,
  });
};
