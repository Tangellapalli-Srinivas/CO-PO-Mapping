new StatusCheck(document.body.dataset.route, function(){
    const response = JSON.parse(this.response);
    console.log(response);
    if(!response.passed){
        return new Error(response.status);
    }
    new Warning(response.status);
    window.location = "/"

});