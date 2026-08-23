document.addEventListener("DOMContentLoaded", function () {
  const ticketTypeField = document.getElementById("id_ticket_type");

  const llaveroField = document.getElementById("id_llavero");

  if (!ticketTypeField || !llaveroField) {
    return;
  }

  async function loadGifts() {
    const ticketTypeId = ticketTypeField.value;

    llaveroField.innerHTML = "";

    if (!ticketTypeId) {
      return;
    }

    try {
      const response = await fetch(`/api/ticket-types/${ticketTypeId}/gifts/`);

      if (!response.ok) {
        throw new Error("No se pudieron obtener los regalos");
      }

      const data = await response.json();

      const llavero = data.regalos?.llavero;

      if (!llavero) {
        return;
      }

      const defaultOption = document.createElement("option");

      defaultOption.value = "";
      defaultOption.textContent = "---------";

      llaveroField.appendChild(defaultOption);

      llavero.list.forEach(function (pais) {
        const option = document.createElement("option");

        option.value = pais;
        option.textContent = pais;

        llaveroField.appendChild(option);
      });
    } catch (error) {
      console.error("Error cargando regalos:", error);
    }
  }

  ticketTypeField.addEventListener("change", loadGifts);
});
