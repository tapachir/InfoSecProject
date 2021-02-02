function makeHttpObject() {
    try {
        return new XMLHttpRequest();
    } catch (error) {
    }
    try {
        return new ActiveXObject("Msxml2.XMLHTTP");
    } catch (error) {
    }
    try {
        return new ActiveXObject("Microsoft.XMLHTTP");
    } catch (error) {
    }

    throw new Error("Could not create HTTP request object.");
}
const button = document.getElementById("get");
button.addEventListener("click", e => {
    const password = document.getElementById("getRequestPassword").value;
    const name = document.getElementById("getRequestName").value;

    const url = "http://0.0.0.0:5000/search?name=" + name+"&password="+password;
    let request = makeHttpObject();
    console.log(url);
    request.open("GET", url, true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState == 4)
            var text = request.responseText;
        document.getElementById("text").innerHTML = text;
    };
});

const button2 = document.getElementById("submit");
button2.addEventListener("click", e => {
    var name = document.getElementById("submitRequestName").value;
    var password = document.getElementById("submitRequestPassword").value;
    var secret = document.getElementById("submitRequestSecret").value;
    // name = "test";
    // password = "test";
    // secret = "test";

    const url = "http://0.0.0.0:5000/register?name=" + name +"&password="+ password +"&secret="+ secret;

    let request = makeHttpObject();
    console.log(url);
    request.open("GET", url, true);

    console.log(2);

    request.send(null);
    console.log(3);

    request.onreadystatechange = function () {
        if (request.readyState == 4)
            var text = request.responseText;
        document.getElementById("text").innerHTML = text;
    };
});
