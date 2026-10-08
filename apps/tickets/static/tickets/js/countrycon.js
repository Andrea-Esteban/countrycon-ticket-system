const escapeHtml = (v) =>
  String(v ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));

function toast(type, text) {            // type: success | warning | danger
  const area = document.getElementById("toast-area");
  if (!area) { alert(text); return; }   // respaldo si falta el contenedor
  const el = document.createElement("div");
  el.className = `toast align-items-center text-bg-${type} border-0`;
  el.setAttribute("role", "status");
  el.innerHTML = `<div class="d-flex"><div class="toast-body"></div>
    <button type="button" class="btn-close btn-close-white me-2 m-auto"
            data-bs-dismiss="toast" aria-label="Cerrar"></button></div>`;
  el.querySelector(".toast-body").textContent = text;
  area.appendChild(el);
  el.addEventListener("hidden.bs.toast", () => el.remove());
  new bootstrap.Toast(el, { delay: type === "danger" ? 7000 : 3500 }).show();
}


function confirmAction({
  title,
  body,
  confirmText = "Confirmar",
  variant = "primary"
}) {
  return new Promise((resolve) => {
    const modalEl = document.getElementById("confirm-modal");

    if (!modalEl) {
      resolve(window.confirm(title));
      return;
    }

    modalEl.querySelector(".modal-title").textContent = title;
    modalEl.querySelector(".modal-body").innerHTML = body;

    const ok = modalEl.querySelector("[data-confirm]");
    ok.textContent = confirmText;
    ok.className = `btn btn-${variant}`;

    const modal = bootstrap.Modal.getOrCreateInstance(modalEl, {
      backdrop: "static",
      keyboard: false
    });

    let answer = false;

    const handleConfirm = () => {
      answer = true;
      modal.hide();
    };

    const handleHidden = () => {
      ok.removeEventListener("click", handleConfirm);
      resolve(answer);
    };

    ok.addEventListener("click", handleConfirm, { once: true });
    modalEl.addEventListener("hidden.bs.modal", handleHidden, { once: true });

    modal.show();
  });
}