<script>
    let college = "";
    let department = "";
    let course = "";
    let section = "";
    
    async function register() {
        const response = await fetch("https://127.0.0.1:5000/register", {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                college,
                department,
                course,
                section
            })
        });
        const data = await response.json();
        console.log(data);
    }

    async function login() {
        const response = await fetch("https://localhost:5000/login", {});
        const data = await response.json();
        console.log(data);
    }
</script>


<h1>EmptyClass</h1>

<button on:click={login}>login</button>

<h2>Register</h2>
<form on:submit|preventDefault={register}>
    <label for="college">College</label>
    <input type="text" id="college" bind:value={college} />
    <label for="department">Department</label>
    <input type="text" id="department" bind:value={department} />
    <label for="course">Course</label>
    <input type="text" id="course" bind:value={course} />
    <label for="section">Section</label>
    <input type="text" id="section" bind:value={section} />
    <button type="submit">Register</button>
</form>