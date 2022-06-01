
function createBlob(){
  const results = document.getElementById("results");
  if(!document.body.dataset.results){
    results.style.display = 'none';
    return 
  }

  results.style.display = 'block';
  const raw = new Blob([document.body.dataset.results], {type: "text/plain"});
  results.href = window.URL.createObjectURL(raw);
  const isOK = Boolean(document.body.dataset.fromStdout);
  
  results.download = isOK ? "results.txt" : "error.txt";
  results.style.border = isOK ? "1px solid green" : "1px solid red";
}

createBlob();


function openModal(wait){
  document.getElementById("wait-until").classList.toggle("modal-open");
  if(wait){
    new StatusCheck("/wait-for-processing", () => openModal(false));
  }
}

if(document.body.dataset.busy){
  openModal(true);
}


function afterSubmit(){
  const response = JSON.parse(this.response);
  openModal(false);

  if(!response.passed){
    return new Error(response.status);
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
