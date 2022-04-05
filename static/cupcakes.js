"use strict";

/** List of jquery objects so we don't have to find them again */

const $cupCakes = $("#cupcakes");
const $cupCakesForm = $("#cupcakes-form");

const API_BASE_URL = "http://localhost:5001"


/** Retrieve list of cupcakes from API  */

async function getCupcakes() {
  const response = await axios({
    // baseURL: API_BASE_URL,
    url: `${API_BASE_URL}/api/cupcakes`,
    method: "GET"
  });

  return response.data.cupcakes;

  // (cupcake => {
  //   return {
  //     id: cupcake.id,
  //     flavor: cupcake.flavor,
  //     size: cupcake.size,
  //     rating: cupcake.rating,
  //     image: cupcake.image
  //   }
  // });
}


// Given a list of cupcakes, display HTML mark up for each and to the DOM
/**  */

function populateCupcakes(cupcakes) {
  for (let cupcake of cupcakes) {
    const $cupcake = $(
      `<div id='${cupcake.id}'>
        <div>
          <img src='${cupcake.image}' alt='${cupcake.flavor}'>
        </div>
        <div>
          <h4> ${cupcake.size} ${cupcake.flavor} Cupcake </h4>
          <h5> ${cupcake.rating} out of 10</h5>
        </div>
      </div>`
    );

    $cupCakes.append($cupcake);
  }
}

// Get cupcakes from API and display them

async function display_cupcakes() {
  $cupCakes.empty();

  const cupcakes = await getCupcakes();
  populateCupcakes(cupcakes);
}

/** Add cupcake to API database */
async function addCupcake(evt) {
  evt.preventDefault();
  const flavor = $('#flavor').val();
  const size = $('#size').val();
  const rating = $('#rating').val();
  const image = $('#image').val();

  const response = await axios.post(
    `${API_BASE_URL}/api/cupcakes`, {
          "flavor": flavor,
          "size": size,
          "rating": rating,
          "image": image
        })
  // const response = await axios({
  //   url: `${API_BASE_URL}/api/cupcakes`,
  //   method: "POST",

  //   data: {
  //     "flavor": flavor,
  //     "size": size,
  //     "rating": rating,
  //     "image": image
  //   }
  // });

  display_cupcakes();
  console.log("Response=", response.data)
  // return response.data;
}


/** Create an event listener for adding a cupcake */

$cupCakesForm.on('click', '.cupcakes-button', addCupcake)

display_cupcakes();