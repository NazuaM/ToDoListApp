// add user id detection so we know which user is logged in 
const urlParams = new URLSearchParams(window.location.search);
const uid = urlParams.get('uid');

if (!uid) {
    alert("Please login first!");
    window.location.href = "/login";
}

const inputBox = document.getElementById("input-box");
const listContainer = document.getElementById("list-container");

async function addTask() {
    const task = inputBox.value.trim();
    if(!task) {
        alert("Please write down a task");
        return;
    }

    // Send task to flask backend
    const response = await fetch('/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
           body: `task=${encodeURIComponent(task)}&uid=${uid}`
    });

    if (response.ok) {
        const newTask = await response.json();
        addTaskToDOM(newTask.id, newTask.task, false);
        inputBox.value = "";
        updateCounters();
    }
    else {
        alert("Failed to save task!");
    }
}

function addTaskToDOM(taskId, taskText, isCompleted) {
    const li = document.createElement("li");
    li.dataset.id = taskId;

    li.innerHTML = `
    <label>
    <input type = "checkbox" ${isCompleted ? 'checked' : ''}>
    <span>${taskText}</span>
    </label>
    <span class= "edit-btn">Edit</span>
    <span class="delete-btn">Delete</span>
    `;

    listContainer.appendChild(li);
    setupTaskEvents(li, taskId);
}

async function setupTaskEvents(li, taskId) {
    const checkbox = li.querySelector("input");
    const editBtn = li.querySelector(".edit-btn");
    const taskSpan = li.querySelector("span");
    const deleteBtn = li.querySelector(".delete-btn");

    checkbox.addEventListener("click",  async function() {
    li.classList.toggle("completed", checkbox.checked);
    await fetch('/update-task', {
        method: 'POST', 
        headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
        body: `task_id=${taskId}&completed=${checkbox.checked}&uid=${uid}`
    });
    updateCounters();
    });

    // Edit - Update task text
    editBtn.addEventListener("click", async function() {
        const newText = prompt("Edit task:", taskSpan.textContent);
        if (newText) {
            taskSpan.textContent = newText;
            await fetch('/update-task-text', {
                method: 'POST',
                headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
                body: `task_id=${taskId}&new_text=${encodeURIComponent(newText)}&uid=${uid}`
            });
        }
    });

    // Delete - Remove task
    deleteBtn.addEventListener("click", async function() {
        if (confirm("Delete this task?")) {
            await fetch('/delete-task', {
                method: 'POST',
                headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
                body: `task_id=${taskId}&uid=${uid}`
            });
            li.remove();
            updateCounters();
        }
    });
}

async function loadTasks() {
    const response = await fetch(`/get-tasks?uid=${uid}`);
    const tasks = await response.json();

    tasks.forEach(task => {
        addTaskToDOM(task.id, task.task, task.completed);
    });
    updateCounters();

}

// Run when page loads
window.addEventListener('DOMContentLoaded', loadTasks);

const completedCounter = document.getElementById("completed-counter");
const uncompletedCounter = document.getElementById("uncompleted-counter");

function updateCounters() {
    const completedTasks = document.querySelectorAll(".completed").length;
    const uncompletedTasks = document.querySelectorAll("li:not(.completed)").length;

    completedCounter.textContent = completedTasks;
    uncompletedCounter.textContent = uncompletedTasks;
}

