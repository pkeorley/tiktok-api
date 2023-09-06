// check ../config.py

const COOKIES = document.cookie.split("; ");
for (const e of COOKIES) {
    const [KEY, VALUE] = e.split("=");
    if (KEY === "msToken") {
        console.log(VALUE); // Copy this value.
    }
}
