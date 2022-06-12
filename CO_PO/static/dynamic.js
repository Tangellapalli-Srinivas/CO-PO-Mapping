function openModal(wait){
  document.querySelectorAll("main > section").forEach((element) => element.classList.toggle("hide"));
  if(wait){
    new StatusCheck("/wait-for-processing", () => {
      openModal(false);
      window.location = "/";
    });
  }
}

if(document.body.dataset.busy){
  openModal(true);
}


function afterSubmit(){
  const response = JSON.parse(this.response);

  if(!response.passed){
    new Error(response.status);
    return openModal(false);
  }

  new Info("Submitted Form");
  window.location = "/";
}

document.getElementById("input").addEventListener("submit", function(e){
  e.preventDefault();
  if(document.body.dataset.results){
    if(!confirm("If you submit this form now, You will lose the results of your previous request.\nSure you want to proceed forward?")){
      return;
    }
  }

  openModal(false);
  new StatusCheck("/submit-input", afterSubmit, "Failed to submit input", new FormData(document.getElementById("input")));
});

document.getElementById("exams").addEventListener("input", function(){
  new Info(`Selected ${this.value} exams`);
})

document.getElementById("raw").addEventListener("change", function(){
  new Info(`Uploaded Excel File ${this.value}`);
})
