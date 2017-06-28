$(document).ready(function() {

    function performLogin() {
        var username = $("#username").val();
        var password = $("#password").val();
        var login_data = {"username":username, "password":password };
        var login_data_json = JSON.stringify(login_data);
        $.ajax({
            url: "http://127.0.0.1:8083/v1/login",
            type: "POST",
            data: login_data_json,
            contentType: "application/json",
            success: function(resp) {
                var token = resp.token;
                console.log("Token: " + token);
                Cookies.set("token", token);
                Cookies.set("tenant_id", "admin");
                return true;
            },
            error: function(err) {
                alert("Error:" + err.status + " " + err.statusText + " " + err.responseText);
                return false;
            }
        });
    }


    function postGraph(params) {
        var token = Cookies.get("token");
        console.log("Token: " + token);
        $.ajax({
            url: "http://127.0.0.1:8083/v1/graphs",
            type: "POST",
            data: JSON.stringify(params.data.graph),
            contentType: "application/json",
            headers: { 'X-Auth-Token': token },
            success: function(resp) {
                var graph_id = resp.id;
                console.log("graph_id: " + graph_id);
                Cookies.set("graph_id", graph_id);
                return true;
            },
            error: function(err) {
                alert("Error:" + err.status + " " + err.statusText + " " + err.responseText);
                return false;
            }
        });
    }


    function updateGraph(params) {
        var token = Cookies.get("token");
        console.log("Token: " + token);
        $.ajax({
            url: "http://127.0.0.1:8083/v1/graphs/"+params.data.graph_id,
            type: "PUT",
            data: JSON.stringify(params.data.graph),
            contentType: "application/json",
            headers: { 'X-Auth-Token': token },
            success: function(resp) {
                var graph_id = resp.id;
                console.log("graph_id: " + graph_id);
                Cookies.set("graph_id", graph_id);
                return true;
            },
            error: function(err) {
                alert("Error:" + err.status + " " + err.statusText + " " + err.responseText);
                return false;
            }
        });
    }

    function deleteGraph(params) {
        var token = Cookies.get("token");
        console.log("Token: " + token);
        console.log("graph_id: " + params.data.graph_id);
        $.ajax({
            url: "http://127.0.0.1:8083/v1/graphs/"+params.data.graph_id,
            type: "DELETE",
            headers: { 'X-Auth-Token': token },
            success: function(resp) {
                console.log("delete success");
                Cookies.remove("graph_id");
                Cookies.remove("tenant_id");
                return true;
            },
            error: function(err) {
                alert("Error:" + err.status + " " + err.statusText + " " + err.responseText);
                return false;
            }
        });
    }

    function migrateState(params) {
        var tenant_id = params.data.tenant_id;
        var graph_id = params.data.graph_id;
        var from_vnf_id = params.data.from_vnf_id;
        var to_vnf_id = params.data.to_vnf_id;
        $.when(getStateFromVnf(tenant_id, graph_id, from_vnf_id))
            .then(function (status) {
                pushStateIntoVnf(tenant_id, graph_id, to_vnf_id, status);
            })
            .fail(function(err){
                console.log(err)
            });

        /*
         var status = getStateFromVnf(tenant_id, graph_id, from_vnf_id);
         console.log("status from var: " + status);
         if(status!== null)
         pushStateIntoVnf(tenant_id, graph_id, to_vnf_id, status);
         */
    }


    function getStateFromVnf(tenant_id, graph_id, vnf_id){
        console.log("tenant_id: " + tenant_id);
        console.log("graph_id: " + graph_id);
        console.log("vnf_id: " + vnf_id);
        var retVal = null;
        $.ajax({
            url: "http://127.0.0.1:8083/v1/status",
            type: "GET",
            headers: { 'tenant_id': tenant_id, 'graph_id': graph_id, 'vnf_id': vnf_id},
            cache: false,
            success: function(resp) {
                console.log("getCurrentStateFromVnf success");
                console.log("status get: " + JSON.stringify(resp));
                retVal = JSON.stringify(resp);
            },
            error: function(err) {
                console.log("getCurrentStateFromVnf failure");
                alert("Error:" + err.status + " " + err.statusText + " " + err.responseText);
            }
        });
        return retVal;
    }

    function pushStateIntoVnf(tenant_id, graph_id, vnf_id, status){
        console.log("status to push: " + status);
        console.log("tenant_id: " + tenant_id);
        console.log("graph_id: " + graph_id);
        console.log("vnf_id: " + vnf_id);
        $.ajax({
            url: "http://127.0.0.1:8083/v1/status",
            type: "PUT",
            data: status,
            cache: false,
            headers: { 'tenant_id': tenant_id, 'graph_id': graph_id, 'vnf_id': vnf_id},
            success: function(resp) {
                console.log("pushStatusIntoVnf success");
                return true
            },
            error: function(err) {
                console.log("pushStatusIntoVnf failure");
                alert("Error:" + err.status + " " + err.statusText + " " + err.responseText);
                return false;
            }
        });
    }

    $("#form-login").submit(performLogin);
    $("#btn-deploy_initial_graph").click({ graph: graph1 }, postGraph);
    $("#btn-deploy_second_nat").click({ graph_id: Cookies.get('graph_id'), graph: graph2 }, updateGraph);
    $("#btn-migrate_state").click({tenant_id: Cookies.get('tenant_id'), graph_id: Cookies.get('graph_id'), from_vnf_id: "00000001", to_vnf_id: "00000002" }, migrateState);
    $("#btn-delete_old_nat").click({ graph_id: Cookies.get('graph_id'), graph: graph3 }, updateGraph);
    $("#btn-undeploy_everything").click({ graph_id: Cookies.get('graph_id') }, deleteGraph);


});