
document.addEventListener("DOMContentLoaded", function () {
    const cartCount = document.getElementById("cart-count");
    const toastContainer = document.getElementById("toast-container");

    // Prevent duplicate requests for the same button.
    const busyButtons = new WeakSet();

    function showMessage(message, isError = false) {
        if (!toastContainer) {
            if (isError) alert(message);
            return;
        }

        const toast = document.createElement("div");
        toast.className = "toast-message";
        toast.textContent = message;

        if (isError) {
            toast.style.background = "#b91c1c";
        }

        toastContainer.appendChild(toast);
        setTimeout(() => toast.remove(), 2500);
    }

    function updateCartCount(count) {
        if (!cartCount || count === undefined || count === null) return;

        cartCount.textContent = String(count);
    }

    async function sendCartRequest(url) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.message || "Unable to update your cart.");
        }

        // Sync the badge with the server's actual cart quantity.
        updateCartCount(data.cart_count);

        return data;
    }

    document.addEventListener("click", async function (event) {
        const addButton = event.target.closest(".add-to-cart-btn");
        const increaseButton = event.target.closest(".increase-btn");
        const decreaseButton = event.target.closest(".decrease-btn");
        const removeButton = event.target.closest(".remove-from-cart-btn");

        const button = addButton || increaseButton || decreaseButton || removeButton;

        if (!button || button.disabled || busyButtons.has(button)) return;

        const productId = button.dataset.productId;

        if (!productId) {
            console.error("Cart button is missing data-product-id.", button);
            showMessage("Could not identify this product.", true);
            return;
        }

        let url;

        if (addButton || increaseButton) {
            url = `/cart/add/${encodeURIComponent(productId)}`;
        } else if (decreaseButton) {
            url = `/cart/decrease/${encodeURIComponent(productId)}`;
        } else {
            url = `/cart/remove/${encodeURIComponent(productId)}`;
        }

        busyButtons.add(button);
        button.disabled = true;

        try {
            const data = await sendCartRequest(url);

            if (addButton) {
                showMessage(data.message || "Added to cart!");
            } else if (increaseButton) {
                showMessage(data.message || "Quantity increased!");
            } else if (decreaseButton || removeButton) {
                // Refresh cart page so quantity, totals, and removed rows
                // stay consistent with the server.
                window.location.reload();
                return;
            }

            // Update quantity/subtotal on the cart page if those elements exist.
            const row = button.closest("[data-cart-item]");
            if (row && data.quantity !== undefined) {
                const quantityElement = row.querySelector(".quantity-value");
                const subtotalElement = row.querySelector(".cart-subtotal");

                if (quantityElement) {
                    quantityElement.textContent = data.quantity;
                }

                if (subtotalElement && data.subtotal !== undefined) {
                    subtotalElement.textContent =
                        "₹" + Number(data.subtotal).toLocaleString("en-IN");
                }
            }
        } catch (error) {
            showMessage(error.message || "Something went wrong.", true);
        } finally {
            busyButtons.delete(button);
            button.disabled = false;
        }
    });
});
