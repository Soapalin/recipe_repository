const imageBase = window.RECIPE_IMAGE_BASE || "/images";

const listView = document.getElementById("listView");
const detailView = document.getElementById("detailView");
const recipeList = document.getElementById("recipeList");
const detailCard = document.getElementById("detailCard");
const backButton = document.getElementById("backButton");

function renderList(recipes) {
  recipeList.innerHTML = "";

  recipes.forEach((recipe) => {
    const card = document.createElement("article");
    card.className = "recipe-card";
    card.tabIndex = 0;
    card.setAttribute("role", "button");
    card.addEventListener("click", () => openDetail(recipe));
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openDetail(recipe);
      }
    });

    card.innerHTML = `
      <img class="recipe-thumb" src="${imageBase}/${recipe.image}" alt="${recipe.title}" />
      <h3 class="card-title">${recipe.title}</h3>
      <p class="card-author">By ${recipe.author}</p>
      <p class="card-summary">${recipe.summary}</p>
      ${
        recipe.url
          ? `<a class="card-link" href="${recipe.url}" target="_blank" rel="noopener">${recipe.url}<span class="link-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path d="M14 3h7v7h-2V6.41l-9.29 9.3-1.42-1.42 9.3-9.29H14V3ZM5 5h6V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-6h-2v6H5V5Z"></path>
              </svg>
            </span></a>`
          : ""
      }
      <div class="meta-row">
        <span class="meta-chip">${recipe.time}</span>
        <span class="meta-chip">Serves ${recipe.servings}</span>
      </div>
    `;

    recipeList.appendChild(card);
  });
}

function openDetail(recipe) {
  listView.style.display = "none";
  detailView.classList.add("active");

  detailCard.innerHTML = `
    <div class="detail-header">
      <img src="${imageBase}/${recipe.image}" alt="${recipe.title}" />
      <div class="detail-meta">
        <h3>${recipe.title}</h3>
        <p class="detail-author">By ${recipe.author}</p>
        <p>${recipe.summary}</p>
        ${
          recipe.url
            ? `<a class="detail-link" href="${recipe.url}" target="_blank" rel="noopener">${recipe.url}<span class="link-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" focusable="false">
                  <path d="M14 3h7v7h-2V6.41l-9.29 9.3-1.42-1.42 9.3-9.29H14V3ZM5 5h6V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-6h-2v6H5V5Z"></path>
                </svg>
              </span></a>`
            : ""
        }
        <div class="meta-row">
          <span class="meta-chip">${recipe.time}</span>
          <span class="meta-chip">Serves ${recipe.servings}</span>
        </div>
        <div class="tag-row">
          ${recipe.tags.map((tag) => `<span class="tag">${tag}</span>`).join("")}
        </div>
      </div>
    </div>
    <div class="detail-columns">
      <div>
        <h4>Ingredients</h4>
        <ul>
          ${recipe.ingredients.map((item) => `<li>${item}</li>`).join("")}
        </ul>
      </div>
      <div>
        <h4>Steps</h4>
        <ol>
          ${recipe.steps.map((step) => `<li>${step}</li>`).join("")}
        </ol>
      </div>
      <div>
        <h4>Notes</h4>
        <p>${recipe.notes}</p>
      </div>
    </div>
  `;

  detailView.scrollIntoView({ behavior: "smooth" });
}

backButton.addEventListener("click", () => {
  detailView.classList.remove("active");
  listView.style.display = "block";
});

fetch("data.json")
  .then((response) => response.json())
  .then((recipes) => renderList(recipes))
  .catch(() => {
    recipeList.innerHTML = "<p>Unable to load recipes.</p>";
  });
