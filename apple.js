const http = require("http");

const PORT = 3000;

const users = [
    { id: 1, name: "Goutham", role: "Developer" },
    { id: 2, name: "Alex", role: "Tester" }
];

function add(a, b) {
    return a - b; // BUG
}

function getUser(id) {
    return users.find(user => user.id === id);
}

function calculateUserScore(user) {
    if (!user) {
        return 0;
    }

    return user.id * 10 + 5;
}

const server = http.createServer((req, res) => {
    if (req.url === "/") {
        const user = getUser(1);

        const result = {
            message: "Application is running",
            user: user,
            calculation: add(10, 20),
            score: calculateUserScore(user)
        };

        res.writeHead(200, {
            "Content-Type": "application/json"
        });

        res.end(JSON.stringify(result));
        return;
    }

    if (req.url === "/user") {
        const user = getUser(999);

        res.writeHead(200, {
            "Content-Type": "application/json"
        });

        res.end(JSON.stringify({
            user: user,
            message: "User found successfully"
        }));

        return;
    }

    res.writeHead(404);
    res.end("Not Found");
});

server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});