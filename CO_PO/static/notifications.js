class Notification{
    element;
    constructor(text){
      this.element = document.createElement("div");
      this.element.classList.add("flag");
      this.element.classList.add("swing-in");
      this.element.textContent = text;
      this.element.addEventListener("click", this.close.bind(this));
      document.querySelector("footer > article.flags").insertAdjacentElement("beforeend", this.element);
    }
    close(){
      this.element.classList.add("closed");
      setTimeout(() => this.element.remove(), 1000);
    }
  }
  
  class Error extends Notification {
    constructor(text){
      super(text);
      this.element.classList.add("error");
    }
  }
  
  class Info extends Notification {
    timer;
    timeout;

    constructor(text, className, timeout){
      super(text);
      
      this.element.classList.add(className || "info");
      this.timeout = timeout || 3000;

      this.timing(true);
      this.element.addEventListener("mouseenter", this.timing.bind(this, false));
      this.element.addEventListener("mouseleave", this.timing.bind(this, true));
    }

    timing(reset){
      reset ? (this.timer = setInterval(this.close.bind(this), this.timeout)) : clearInterval(this.timer);
    }
  }


  class Warning extends Info{
    constructor(text, timeout){
        super(text, "warning", timeout || 6000);
    }
  }

class StatusCheck{
  route; listener; data;
  tries;
  error_msg;
  
  constructor(route, listener, error_msg, data){
    this.route = route;
    this.listener = listener;
    this.data = data;
    this.error_msg = error_msg;
    this.tries = 0;
    this.sendRequest();
  }

  sendRequest(){
    const request = new XMLHttpRequest();
    request.open(this.data ? "POST" : "GET", this.route, true);
    request.addEventListener("load", this.listener || StatusCheck.check);
    request.addEventListener("error", this.handleError.bind(this));
    request.send(this.data)

    this.tries++;
    return request;
  }

  handleError(){
    if(this.tries <= 3){
      return new Error(`Failed to connect to server for the route: ${this.route}, Please try again later`);
    }
    new Warning(`Tried to connect to server for the route: ${this.route} for ${this.tries} times. Trying one more time`);
    return this.sendRequest()
  }

  static check(){
    console.log(this, this.route);
    const response = JSON.parse(this.response);
    let refresh = false;

    if(response["force_refresh"]){
      refresh = true;
    }
    else if(response["ask_refresh"]){
        refresh = confirm("Server is ahead of us! Seems like you made a request from another tab!!! Want to refresh!\nRefreshing will undo things in this tab.")
    }

    new Warning(response.status);
    return refresh  ? (window.location = "/") : null;
  }


  static closeSession(route, e){
    const response = JSON.parse(e.srcElement.response);
    const warn = response["force_refresh"] || response["ask_refresh"];

    if(warn){
      new Warning("It seems your Matlab Engine is busy!, Closing now would force close their tasks");
    }
    
    
    if(!confirm("Are you sure you want to close your session?")){
      return;
    }

    if(!route){
      return new StatusCheck("/close-session", () => new Error("You can close this window"));
    }
    else{
      window.location = route;
    }
  }
}

document.getElementById("status").addEventListener('click', () => new StatusCheck("/get-status"));
document.getElementById("restart").addEventListener("click", () => new StatusCheck("/get-status", function(_){ StatusCheck.closeSession("/restart", _)}));
document.getElementById("close").addEventListener("click", () => new StatusCheck("/get-status", function(_){ StatusCheck.closeSession("", _)}));
document.getElementById("switch").addEventListener("input", function(){
  new StatusCheck(`/auto-updates?auto-update=${this.checked ? "1" : "0"}`, () => new Info("Response Saved"), "Failed to contact Server");
});


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
