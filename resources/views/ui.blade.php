<html>
<head>
    <title> main ui </title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
          integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
<div class="container" style="max-width: 1500px">
    <div class="row">
        <div class="col-xl p-3">
            <div class="form-group">
                <label for="price">price</label>
                <input class="form-control" type="number" id="price" placeholder="Enter price"/>
            </div>
            <div class="form-group">
                <label for="description">description</label>
                <input class="form-control" type="text" id="description" placeholder="Enter description"/>
            </div>
            <div class="form-group">
                <label for="kindTitle">kind title</label>
                <input class="form-control" type="text" id="kindTitle" placeholder="Enter kind title"/>
            </div>
            <div class="form-group">
                <label for="typeTitle">type title</label>
                <input class="form-control" type="text" id="typeTitle" placeholder="Enter type title"/>
            </div>
            <div class="form-group">
                <label for="category">category</label>
                <input class="form-control" type="text" id="category" placeholder="Enter category"/>
            </div>
            <div class="form-group">
                <label for="page">page</label>
                <input class="form-control" type="text" id="page" placeholder="Enter page number"/>
            </div>
            <button class="btn btn-primary text-white" onclick="search(event)">search</button>
        </div>

        <div class="col-xl p-3">
            <label class="mt-2 mb-2">If you don't fill in text inputs we show all the data.</label><br/>
            <div class="form-group">
                <label for="items">item id</label>
                <input class="form-control" type="number" id="items" placeholder="Enter item id"/>
            </div>
            <button class="btn btn-primary text-white" onclick="showItems(event)">Get Items</button>
            <hr/>

            <div class="form-group">
                <label for="kinds">kind id</label>
                <input class="form-control" type="number" id="kinds" placeholder="Enter kind id"/>
            </div>
            <button class="btn btn-primary text-white" onclick="showKinds(event)">Get Kinds</button>
            <hr/>

            <div class="form-group">
                <label for="types">type id</label>
                <input class="form-control" type="number" id="types" placeholder="Enter type id"/>
            </div>
            <button class="btn btn-primary text-white" onclick="showTypes(event)">Get Types</button>
        </div>

        <div class="col-xl p-3" id="item-div">
            <div class="form-group">
                <label for="item_id">id</label>
                <input class="form-control" type="number" id="item_id" placeholder="Enter item id"/>
            </div>
            <div class="form-group">
                <label for="item_price">price</label>
                <input class="form-control" type="number" id="item_price" placeholder="Enter item price"/>
            </div>
            <div class="form-group">
                <label for="item_description">description</label>
                <input class="form-control" type="text" id="item_description" placeholder="Enter item description"/>
            </div>
            <div class="form-group">
                <label for="item_kind_id">kind id</label>
                <input class="form-control" type="number" id="item_kind_id" placeholder="Enter kind id"/>
            </div>
            <button class="btn btn-primary text-white" onclick="createItem(event)">Create</button>
            <button class="btn btn-success text-white" onclick="updateItem(event)">Update</button>
            <button class="btn btn-danger text-white" onclick="deleteItem(event)">Delete</button>
        </div>

        <div class="col-xl p-3" id="type-div">
            <div class="form-group">
                <label for="type_id">id</label>
                <input class="form-control" type="number" id="type_id" placeholder="Enter type id"/>
            </div>
            <div class="form-group">
                <label for="type_title">title</label>
                <input class="form-control" type="text" id="type_title" placeholder="Enter type title"/>
            </div>
            <div class="form-group">
                <label for="type_category">category</label>
                <input class="form-control" type="text" id="type_category" placeholder="Enter type category"/>
            </div>
            <button class="btn btn-primary text-white" onclick="createType(event)">Create</button>
            <button class="btn btn-success text-white" onclick="updateType(event)">Update</button>
            <button class="btn btn-danger text-white" onclick="deleteType(event)">Delete</button>
        </div>

        <div class="col-xl p-3" id="kind-div">
            <div class="form-group">
                <label for="kind_id">id</label>
                <input class="form-control" type="number" id="kind_id" placeholder="Enter kind id"/>
            </div>
            <div class="form-group">
                <label for="kind_title">title</label>
                <input class="form-control" type="text" id="kind_title" placeholder="Enter kind title"/>
            </div>
            <div class="form-group">
                <label for="kind_min_price">min price</label>
                <input class="form-control" type="number" id="kind_min_price" placeholder="Enter min price"/>
            </div>
            <div class="form-group">
                <label for="kind_max_price">max price</label>
                <input class="form-control" type="number" id="kind_max_price" placeholder="Enter max price"/>
            </div>
            <div class="form-group">
                <label for="kind_item_type_id">type id</label>
                <input class="form-control" type="number" id="kind_item_type_id" placeholder="Enter type id"/>
            </div>
            <button class="btn btn-primary text-white" onclick="createKind(event)">Create</button>
            <button class="btn btn-success text-white" onclick="updateKind(event)">Update</button>
            <button class="btn btn-danger text-white" onclick="deleteKind(event)">Delete</button>
            <hr/>

            <button class="btn btn-danger text-white w-50" onclick="logout(event)">logout</button>
        </div>

        <div class="col-xl p-3" id="login-div">
            <div class="form-group">
                <label for="email">email</label>
                <input class="form-control" type="email" id="email" placeholder="Enter email"/>
            </div>
            <div class="form-group">
                <label for="password">password</label>
                <input class="form-control" type="password" id="password" placeholder="Enter password"/>
            </div>
            <button class="btn btn-success" onclick="login(event)">Login</button>
        </div>
        <div class="col-xl p-3" id="signup-div">
            <div class="form-group">
                <label for="signup_email">email</label>
                <input class="form-control" type="email" id="signup_email" placeholder="Enter email"/>
            </div>
            <div class="form-group">
                <label for="signup_name">name</label>
                <input class="form-control" type="text" id="signup_name" placeholder="Enter name"/>
            </div>
            <div class="form-group">
                <label for="signup_password">password</label>
                <input class="form-control" type="password" id="signup_password" placeholder="Enter password"/>
            </div>
            <div class="form-group">
                <label for="signup_password_confirmation">password confirmation</label>
                <input class="form-control" type="password" id="signup_password_confirmation" placeholder="Enter password again"/>
            </div>
            <button class="btn btn-success" onclick="signup(event)">Sign Up</button>
        </div>

    </div>
</div>
<div class="container" style="max-width: 1500px">
    <div id="results"></div>
</div>
</body>
<script>

    const token = getCookie('token');
    if (token.length !== 0) {
        document.getElementById('login-div').setAttribute('hidden', 'true');
        document.getElementById('signup-div').setAttribute('hidden', 'true');
    } else {
        document.getElementById('item-div').setAttribute('hidden', 'true');
        document.getElementById('kind-div').setAttribute('hidden', 'true');
        document.getElementById('type-div').setAttribute('hidden', 'true');
    }

    let xhttp = new XMLHttpRequest();

    function search(e) {
        e.preventDefault();

        const price = document.getElementById("price").value;
        const description = document.getElementById("description").value;
        const kindTitle = document.getElementById("kindTitle").value;
        const typeTitle = document.getElementById("typeTitle").value;
        const category = document.getElementById("category").value;
        const page = document.getElementById("page").value;

        let query = "";
        if (price.length !== 0)
            query = query + "price=" + price + "&";
        if (description.length !== 0)
            query = query + "description=" + description + "&";
        if (kindTitle.length !== 0)
            query = query + "kindTitle=" + kindTitle + "&";
        if (typeTitle.length !== 0)
            query = query + "typeTitle=" + typeTitle + "&";
        if (category.length !== 0)
            query = query + "category=" + category + "&";
        if (page.length !== 0)
            query = query + "page=" + page + "&";

        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status % 200 === 0) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        // xhttp.setRequestHeader('Content-Type', 'application/json');
        // xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.open('GET', 'http://localhost:8000/api/search?' + query);
        xhttp.send();
    }

    function showItems(e) {
        e.preventDefault();
        const item_id = document.getElementById("items").value;
        let query = "";
        if (item_id.length !== 0)
            query = query + "/" + item_id;

        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status % 200 === 0) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, Object.values(data.data));
            }
        };
        xhttp.open('GET', 'http://localhost:8000/api/items' + query);
        xhttp.send();
    }

    function login(e) {
        const email = document.getElementById("email").value;
        const pass = document.getElementById("password").value;

        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status % 200 === 0) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('POST', 'http://localhost:8000/api/auth/login', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.send(JSON.stringify({
            "email": email,
            "password": pass,
        }));
    }

    function signup(e) {
        e.preventDefault();
        const email = document.getElementById("signup_email").value;
        const name = document.getElementById("signup_name").value;
        const pass = document.getElementById("signup_password").value;
        const passcon = document.getElementById("signup_password_confirmation").value;

        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('POST', 'http://localhost:8000/api/auth/signup', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.send(JSON.stringify({
            "email": email,
            "name": name,
            "password": pass,
            "password_confirmation": passcon
        }));
    }

    function logout(e) {
        e.preventDefault();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                document.cookie = "token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
                location.reload();
            }
        };
        xhttp.open('GET', 'http://localhost:8000/api/auth/logout', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        xhttp.send();
    }

    function createItem(e) {
        e.preventDefault();
        const price = document.getElementById("item_price").value;
        const description = document.getElementById("item_description").value;
        const kind_id = document.getElementById("item_kind_id").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('POST', 'http://localhost:8000/api/items', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        xhttp.send(JSON.stringify({
            "price": price,
            "description": description,
            "kind_id": kind_id,
        }));
    }

    function updateItem(e) {
        e.preventDefault();
        const id = document.getElementById("item_id").value;
        const price = document.getElementById("item_price").value;
        const description = document.getElementById("item_description").value;
        const kind_id = document.getElementById("item_kind_id").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                console.log(xhttp.responseText);
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('PUT', 'http://localhost:8000/api/items/' + id, true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        let body = {};
        if (price.length !== 0)
            body.price = price;
        if (description.length !== 0)
            body.description = description;
        if (kind_id.length !== 0)
            body.kind_id = kind_id;
        xhttp.send(JSON.stringify(body));
    }

    function deleteItem(e) {
        e.preventDefault();
        const id = document.getElementById("item_id").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('DELETE', 'http://localhost:8000/api/items/' + id, true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        xhttp.send();
    }

    function createKind(e) {
        e.preventDefault();
        const title = document.getElementById("kind_title").value;
        const min_price = document.getElementById("kind_min_price").value;
        const max_price = document.getElementById("kind_max_price").value;
        const type_id = document.getElementById("kind_item_type_id").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('POST', 'http://localhost:8000/api/kinds', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        xhttp.send(JSON.stringify({
            "title": title,
            "min_price": min_price,
            "max_price": max_price,
            "item_type_id": type_id
        }));
    }

    function updateKind(e) {
        e.preventDefault();
        const id = document.getElementById("kind_id").value;
        const title = document.getElementById("kind_title").value;
        const min_price = document.getElementById("kind_min_price").value;
        const max_price = document.getElementById("kind_max_price").value;
        const type_id = document.getElementById("kind_item_type_id").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('PUT', 'http://localhost:8000/api/kinds/' + id, true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        let body = {};
        if (title.length !== 0)
            body.title = title;
        if (min_price.length !== 0)
            body.min_price = min_price;
        if (max_price.length !== 0)
            body.max_price = max_price;
        if (type_id.length !== 0)
            body.type_id = type_id;
        xhttp.send(JSON.stringify(body));
    }

    function deleteKind(e) {
        e.preventDefault();
        const id = document.getElementById("kind_id").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('DELETE', 'http://localhost:8000/api/kinds/' + id, true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        xhttp.send();
    }

    function createType(e) {
        e.preventDefault();
        const title = document.getElementById("type_title").value;
        const category = document.getElementById("type_category").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('POST', 'http://localhost:8000/api/itemTypes', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        xhttp.send(JSON.stringify({
            "title": title,
            "category": category,
        }));
    }

    function updateType(e) {
        e.preventDefault();
        const id = document.getElementById("type_id").value;
        const title = document.getElementById("type_title").value;
        const category = document.getElementById("type_category").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('PUT', 'http://localhost:8000/api/itemTypes/' + id, true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        let body = {};
        if (id.length !== 0)
            body.id = id;
        if (title.length !== 0)
            body.title = title;
        if (category.length !== 0)
            body.category = category;
        xhttp.send(JSON.stringify(body));
    }

    function deleteType(e) {
        e.preventDefault();
        const id = document.getElementById("type_id").value;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status / 100 === 2) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, data.data);
            }
        };
        xhttp.open('DELETE', 'http://localhost:8000/api/itemTypes/' + id, true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhttp.setRequestHeader('Authorization', 'Bearer ' + getCookie('token'));
        xhttp.send();
    }

    function showKinds(e) {
        e.preventDefault();
        const kind_id = document.getElementById("kinds").value;
        let query = "";
        if (kind_id.length !== 0)
            query = query + "/" + kind_id;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, Object.values(data.data));
            }
        };
        xhttp.open('GET', 'http://localhost:8000/api/kinds' + query);
        xhttp.send();
    }

    function showTypes(e) {
        e.preventDefault();
        const type_id = document.getElementById("types").value;
        let query = "";
        if (type_id.length !== 0)
            query = query + "/" + type_id;
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                let data = JSON.parse(xhttp.responseText);
                showResult(data.type, Object.values(data.data));
            }
        };
        xhttp.open('GET', 'http://localhost:8000/api/itemTypes' + query);
        xhttp.send();
    }

    function showResult(type, data) {
        const resultDiv = document.getElementById("results");
        if (type === 'search-result' || type === 'list') {

            data = Object.values(data);
            const result = document.createElement("table");

            resultDiv.setAttribute("class", "table-responsive");
            result.setAttribute("class", "table table-striped table-bordered");
            resultDiv.innerHTML = "";
            result.setAttribute("border", "1");

            const list_length = type === 'search-result' ? data.length - 2 : data.length;

            if (list_length > 0) {
                let heads = Object.keys(data[0]);
                const head = document.createElement("tr");
                heads.forEach(function (item) {
                    const col = document.createElement("th");
                    let text = document.createTextNode(item);
                    col.appendChild(text);
                    head.appendChild(col);
                });
                result.appendChild(head);
            }


            for (let i = 0; i < list_length; i++) {
                const row = document.createElement("tr");
                let datum = Object.values(data[i]);
                datum.forEach(function (item) {
                    const col = document.createElement("td");
                    let text = document.createTextNode(item);
                    col.appendChild(text);
                    row.appendChild(col);
                });
                result.appendChild(row);
            }
            resultDiv.appendChild(result);
        }

        if (type === 'message') {
            resultDiv.innerHTML = "";
            let p = document.createElement("p");
            let text = document.createTextNode(data);
            p.appendChild(text);
            resultDiv.appendChild(p);
        }

        if (type === 'auth') {
            document.cookie = 'token=' + escape(data.access_token);
            location.reload();
        }
    }

    function getCookie(cname) {
        let name = cname + "=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const ca = decodedCookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
</script>
</html>
