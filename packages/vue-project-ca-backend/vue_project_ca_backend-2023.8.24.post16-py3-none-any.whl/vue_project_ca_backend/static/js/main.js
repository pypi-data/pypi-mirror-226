var userinfo = "";


function GetUserInfo(token) {
    $.ajax({
        url: "/userinfo",
        type: "get",
        async: false,
        headers: {
            "Authorization": "Bearer " + token
        },
        success: function (res) {
            if (res.code === 200) {
                userinfo = res;
            }
        },
        fail: function (res) {
            console.log(res);
        }
    });
}


function CheckLogin() {
    let token = localStorage.getItem("TOKEN");
    if (token === null) {
        return false;
    }

    GetUserInfo(token);
    return !(userinfo === "" || userinfo === undefined);

}