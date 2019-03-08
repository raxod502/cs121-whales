var modelName = null;
var modelList = null;
var userColor = null;
var modelRequest = {
  command: "list_models"
};

// Start when html has been loaded
$(document).ready(function() {
  modelList = document.getElementById("select-model");
  colorList = document.getElementById("select-color");
  // Get list of models from API
  apiRequest(modelRequest, onModelRequestComplete);
  $("#playBtn").on("click", function() {
    // Get the user-selected model and color values and navigate to chess.html
    modelName = modelList.options[modelList.selectedIndex].value;
    userColor = colorList.options[colorList.selectedIndex].value;
    sessionStorage.setItem("modelName", modelName);
    sessionStorage.setItem("userColor", userColor);
    window.location.href = "/play";
  });
});

var onModelRequestComplete = function(msg) {
  console.log(msg);
  for (const model of msg.models) {
    modelList.options[modelList.options.length] = new Option(
      model.displayName,
      model.internalName
    );
  }
};
