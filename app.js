document.getElementById("study-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent form reload

    const major = document.getElementById("major").value.trim();
    const interests = document.getElementById("interests").value.trim();

    // ✅ Validate input
    if (!major || !interests) {
        alert("Please enter both your major and study interests.");
        return;
    }

    try {
        // ✅ Send the form data to the backend API
        const response = await fetch("http://localhost:5000/match-students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ major, interests })
        });

        // ✅ Handle non-200 responses
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response from server:", data); // Debugging

        // ✅ Display matched users
        const partnersList = document.getElementById("study-partners");
        partnersList.innerHTML = "";

        if (data.matchedUsers && data.matchedUsers.length > 0) {
            data.matchedUsers.forEach(user => {
                const listItem = document.createElement("li");
                listItem.textContent = `User ID: ${user.user_id} | Major: ${user.major}`;
                partnersList.appendChild(listItem);
            });
        } else {
            // ✅ Handle case when no matches are found
            partnersList.innerHTML = "<li>No matching study partners found.</li>";
        }
    } catch (error) {
        console.error("Fetch error:", error);
        alert("Something went wrong! Please check your connection and try again.");
    }
});
