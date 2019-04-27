"use strict";

function isObject(val) {
  /**
   * Return True if val is a non-null object
   */
  return typeof val === "object" && val !== null;
}

function isString(val) {
  /**
   * Return True if val is a string
   * NOTE: could be empty
   */
  return typeof val === "string";
}

function isArray(val) {
  /**
   * Return True if val is an array
   */

  return Array.isArray(val);
}

function capitalize(str) {
  /**
   * Capitalize the first letter of a string.
   */
  return str[0].toUpperCase() + str.slice(1);
}

function friendlyErrorMessage(rawMessage) {
  /**
   * Take "rawMessage", return in a nice string that can be displayed
   * to users.
   */
  return (
    'W.H.A.L.E.S. encountered an unexpected error: "' +
    capitalize(rawMessage) +
    '". Unfortunately, ' +
    "we don't know how to fix it. Sorry! Your " +
    "best bet is to reload the page and see if things " +
    "are fixed."
  );
}

function apiRequest(request, callback, onError) {
  /**
   *Send api request
   *If valid request, perform callback
   *Otherwise, perform onError
   */
  if (!onError) {
    const up = "devastating error";
    alert("No error callback provided!!");
    throw up;
  }
  return $.ajax({
    method: "POST",
    url: "/api/v1/http",
    contentType: "application/json",
    data: JSON.stringify(request),
    // Parse the returned response into JSON.
    dataType: "json",
    success: data => {
      if (!isObject(data)) {
        onError("API response is not an object");
      } else if (!data.hasOwnProperty("error")) {
        onError("API response missing 'error' key");
      } else if (data.error) {
        onError(data.error);
      } else {
        callback(data);
      }
    },
    error: (xhr, textStatus, errorThrown) => {
      // Check first if an HTTP error occurred, and report the status
      // text for it (confusingly named errorThrown) if so. Otherwise,
      // fall back to the more generic textStatus argument
      if (errorThrown) {
        onError(errorThrown.toLowerCase());
      } else {
        onError(textStatus);
      }
    }
  });
}

function apiListModels(callback, onError) {
  /**
   * Wrapper to list models via the api
   */
  apiRequest(
    {
      command: "list_models"
    },
    response => {
      if (!isArray(response.models)) {
        onError("API response for 'list_models' was not an array");
        return;
      }
      for (const model of response.models) {
        if (!isObject(model)) {
          onError("API response for 'list_models' contained non-object");
          return;
        }
        for (const key of ["displayName", "internalName"]) {
          if (!model.hasOwnProperty(key)) {
            onError(`API response for 'list_models' missing key '${key}'`);
            return;
          }
          if (!isString(model[key])) {
            onError(
              `API response for 'list_models' has non-string for key '${key}'`
            );
            return;
          }
        }
      }
      callback(response.models);
    },
    onError
  );
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

//Below handles clicks on screen, hashing the location
$(".homeLink").each((index, value) => {
  $(value).on("click", () => {
    window.location.href = "/" + window.location.hash;
  });
});
