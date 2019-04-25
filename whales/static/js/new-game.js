const modelDropdown = "#select-model";
const colorDropdown = "#select-color";

let retrievedModels = false;
let models = null;

function initButton(id, path) {
  /**
   *Initialize buttons for page
   *takes 'id', the name from HTML, and 'path', the name of the function to call
   *set the hash for color and model
   */

  $(`#${id}`).on("click", () => {
    const data = {
      playerColor: $(colorDropdown).val()
    };
    if (retrievedModels) {
      data.backendModel = $(modelDropdown).val();
    } else if (model) {
      data.backendModel = prevModel;
    }
    window.location.href = `/${path}#` + encodeHash(data);
  });
}

const prevData = decodeHash(window.location.hash.substr(1));
const prevColor = prevData.playerColor;
const prevModel = prevData.backendModel;

if (prevColor === "w" || prevColor === "b") {
  $(colorDropdown).val(prevColor);
}

function displayError(error) {
  /**
   * Display an error if the models can't be retrieved.
   */
  $("playBtn").off();
  alert(
    friendlyErrorMessage(
      "couldn't get the list of models: " + capitalize(error)
    )
  );
}

apiListModels(respModels => {
  /**
   * Return a list of all models
   */
  models = respModels;
  $(modelDropdown).options = [];
  for (const model of models) {
    $(modelDropdown).append(new Option(model.displayName, model.internalName));
    if (model.internalName === prevModel) {
      $(modelDropdown).val(prevModel);
    }
  }
  retrievedModels = true;
}, displayError);

initButton("playBtn", "play");
initButton("aboutBtn", "about");
