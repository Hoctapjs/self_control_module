(function () {
    "use strict";

    var ROOT_SELECTOR = ".o_psm_0215_portal";
    var SIGNATURE_INPUT_BY_CANVAS = {
        "employee-pad": "employee_sig_data",
        "manager-pad": "manager_sig_data",
        "witness-pad": "witness_sig_data",
    };

    function ready(fn) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", fn);
        } else {
            fn();
        }
    }

    function each(list, callback) {
        Array.prototype.forEach.call(list || [], callback);
    }

    function getSubmitter(ev) {
        return ev.submitter || document.activeElement;
    }

    function showFlash(root, message, kind) {
        var slot = root.querySelector(".psm-flash-slot") || root;
        var alert = document.createElement("div");
        alert.className = "psm-alert psm-alert--" + (kind || "warning");
        alert.setAttribute("role", kind === "danger" ? "alert" : "status");
        alert.innerHTML = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i><span></span>';
        alert.querySelector("span").textContent = message;
        slot.prepend(alert);
        window.setTimeout(function () {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 5000);
    }

    function initAutoResizeTextareas(root) {
        function resize(textarea) {
            textarea.style.height = "auto";
            textarea.style.height = textarea.scrollHeight + "px";
        }

        each(root.querySelectorAll("textarea.psm-autosize"), function (textarea) {
            resize(textarea);
            textarea.addEventListener("input", function () {
                resize(textarea);
            });
        });
    }

    function fieldHasValue(field, form) {
        if (field.disabled) {
            return true;
        }
        if (field.type === "radio") {
            return Boolean(form.querySelector('input[name="' + field.name + '"]:checked'));
        }
        if (field.type === "checkbox") {
            return field.checked;
        }
        if (field.type === "file") {
            return field.files && field.files.length > 0;
        }
        return Boolean((field.value || "").trim());
    }

    function initFormProgress(root) {
        var nav = root.querySelector(".psm-form-progress");
        if (!nav) {
            return;
        }

        var dots = nav.querySelectorAll(".psm-form-progress__dot");
        var sections = [];

        each(dots, function (dot) {
            var target = root.querySelector(dot.getAttribute("href"));
            if (target) {
                sections.push(target);
                dot.addEventListener("click", function (ev) {
                    ev.preventDefault();
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                });
            }
        });

        function setActive(section) {
            each(dots, function (dot) {
                dot.classList.toggle("is-active", dot.getAttribute("href") === "#" + section.id);
            });
        }

        function refreshDoneState() {
            each(dots, function (dot) {
                var section = root.querySelector(dot.getAttribute("href"));
                if (!section) {
                    return;
                }
                var required = section.querySelectorAll("[required]");
                var done = required.length > 0;
                each(required, function (field) {
                    if (!fieldHasValue(field, field.form || root)) {
                        done = false;
                    }
                });
                dot.classList.toggle("is-done", done);
            });
        }

        if ("IntersectionObserver" in window) {
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        setActive(entry.target);
                    }
                });
            }, { rootMargin: "-30% 0px -55% 0px", threshold: 0.01 });
            sections.forEach(function (section) {
                observer.observe(section);
            });
        }

        root.addEventListener("input", refreshDoneState);
        root.addEventListener("change", refreshDoneState);
        refreshDoneState();
    }

    function initUnsavedGuard(root) {
        var forms = root.querySelectorAll("form");
        if (!forms.length) {
            return;
        }

        var dirty = false;
        var submitting = false;

        each(forms, function (form) {
            form.addEventListener("input", function () {
                dirty = true;
            });
            form.addEventListener("change", function () {
                dirty = true;
            });
            form.addEventListener("submit", function (ev) {
                submitting = true;
                window.setTimeout(function () {
                    if (ev.defaultPrevented) {
                        submitting = false;
                    }
                }, 0);
            });
        });

        window.addEventListener("beforeunload", function (ev) {
            if (!dirty || submitting) {
                return;
            }
            ev.preventDefault();
            ev.returnValue = "";
        });
    }

    function openRejectModal(root, onConfirm) {
        var previousFocus = document.activeElement;
        var modal = document.createElement("div");
        modal.className = "psm-confirm-modal";
        modal.setAttribute("role", "presentation");
        modal.innerHTML = [
            '<div class="psm-confirm-modal__backdrop" data-psm-modal-cancel></div>',
            '<div class="psm-confirm-modal__dialog" role="dialog" aria-modal="true" aria-labelledby="psm_reject_confirm_title" aria-describedby="psm_reject_confirm_desc">',
            '<button type="button" class="psm-confirm-modal__close" data-psm-modal-cancel aria-label="Đóng">&times;</button>',
            '<div class="psm-confirm-modal__icon" aria-hidden="true"><i class="fa fa-exclamation"></i></div>',
            '<div class="psm-confirm-modal__body">',
            '<h5 id="psm_reject_confirm_title" class="psm-confirm-modal__title">Xác nhận từ chối kỷ luật</h5>',
            '<p id="psm_reject_confirm_desc" class="psm-confirm-modal__text">Bạn chắc chắn muốn từ chối hình thức kỷ luật này? Hệ thống sẽ gửi lý do từ chối cho quản lý xử lý lại.</p>',
            "</div>",
            '<div class="psm-confirm-modal__actions">',
            '<button type="button" class="psm-btn psm-btn--secondary" data-psm-modal-cancel>Hủy</button>',
            '<button type="button" class="psm-btn psm-btn--danger" data-psm-modal-confirm>Xác nhận từ chối</button>',
            "</div>",
            "</div>",
        ].join("");

        function closeModal() {
            document.removeEventListener("keydown", onKeydown);
            modal.remove();
            if (previousFocus && previousFocus.focus) {
                previousFocus.focus();
            }
        }

        function onKeydown(ev) {
            if (ev.key === "Escape") {
                closeModal();
            }
        }

        root.appendChild(modal);
        document.addEventListener("keydown", onKeydown);

        each(modal.querySelectorAll("[data-psm-modal-cancel]"), function (button) {
            button.addEventListener("click", closeModal);
        });

        modal.querySelector("[data-psm-modal-confirm]").addEventListener("click", function () {
            closeModal();
            onConfirm();
        });

        window.setTimeout(function () {
            var confirmButton = modal.querySelector("[data-psm-modal-confirm]");
            if (confirmButton) {
                confirmButton.focus();
            }
        }, 0);
    }

    function initRejectConfirm(root) {
        each(root.querySelectorAll('[data-psm-confirm="reject"]'), function (button) {
            var form = button.form;
            if (!form) {
                return;
            }
            form.addEventListener("submit", function (ev) {
                var submitter = getSubmitter(ev);
                if (submitter !== button) {
                    return;
                }
                if (form.getAttribute("data-psm-reject-confirmed") === "1") {
                    form.removeAttribute("data-psm-reject-confirmed");
                    return;
                }
                var note = root.querySelector("#employee_reject_note");
                if (!note || !(note.value || "").trim()) {
                    ev.preventDefault();
                    showFlash(root, "Vui lòng nhập lý do từ chối trước khi gửi.", "danger");
                    if (note) {
                        note.focus();
                    }
                    return;
                }
                ev.preventDefault();
                openRejectModal(root, function () {
                    form.setAttribute("data-psm-reject-confirmed", "1");
                    if (form.requestSubmit) {
                        form.requestSubmit(button);
                        return;
                    }
                    if (button.name) {
                        var proxy = document.createElement("input");
                        proxy.type = "hidden";
                        proxy.name = button.name;
                        proxy.value = button.value;
                        form.appendChild(proxy);
                    }
                    form.submit();
                });
            });
        });
    }

    function initSubmitLoading(root) {
        each(root.querySelectorAll("form[data-psm-loading='1']"), function (form) {
            form.addEventListener("submit", function (ev) {
                if (ev.defaultPrevented) {
                    return;
                }
                var submitter = getSubmitter(ev);
                var buttons = form.querySelectorAll("button[type='submit']");
                if (submitter && submitter.classList) {
                    submitter.classList.add("is-loading");
                }
                if (submitter && submitter.name) {
                    each(form.querySelectorAll("input[data-psm-submitter-proxy='1']"), function (input) {
                        input.remove();
                    });
                    var proxy = document.createElement("input");
                    proxy.type = "hidden";
                    proxy.name = submitter.name;
                    proxy.value = submitter.value;
                    proxy.setAttribute("data-psm-submitter-proxy", "1");
                    form.appendChild(proxy);
                }
                each(buttons, function (button) {
                    button.disabled = true;
                });
                window.setTimeout(function () {
                    if (submitter && submitter.classList) {
                        submitter.classList.remove("is-loading");
                    }
                    each(buttons, function (button) {
                        button.disabled = false;
                    });
                }, 5000);
            });
        });
    }

    function canvasPoint(canvas, ev) {
        var rect = canvas.getBoundingClientRect();
        var point = ev.touches ? ev.touches[0] : ev;
        return {
            x: point.clientX - rect.left,
            y: point.clientY - rect.top,
        };
    }

    function bindDrawing(canvas) {
        var ctx = canvas.getContext("2d");
        var drawing = false;
        var last = null;

        ctx.strokeStyle = "#111111";
        ctx.lineWidth = 4;
        ctx.lineCap = "round";

        function start(ev) {
            drawing = true;
            last = canvasPoint(canvas, ev);
        }

        function move(ev) {
            if (!drawing || !last) {
                return;
            }
            ev.preventDefault();
            var current = canvasPoint(canvas, ev);
            ctx.beginPath();
            ctx.moveTo(last.x, last.y);
            ctx.lineTo(current.x, current.y);
            ctx.stroke();
            last = current;
        }

        function end() {
            drawing = false;
            last = null;
        }

        canvas.addEventListener("mousedown", start);
        canvas.addEventListener("mousemove", move);
        window.addEventListener("mouseup", end);
        canvas.addEventListener("touchstart", start, { passive: true });
        canvas.addEventListener("touchmove", move, { passive: false });
        window.addEventListener("touchend", end);
    }

    function updateSignatureInput(originalCanvas) {
        var inputId = SIGNATURE_INPUT_BY_CANVAS[originalCanvas.id];
        var input = inputId ? document.getElementById(inputId) : null;
        if (input) {
            input.value = originalCanvas.toDataURL("image/png").split(",")[1];
        }
    }

    function initSignatureFullscreen(root) {
        each(root.querySelectorAll(".psm-signature-fullscreen-btn"), function (button) {
            button.addEventListener("click", function () {
                var canvasId = button.getAttribute("data-canvas-id");
                var originalCanvas = canvasId ? document.getElementById(canvasId) : null;
                if (!originalCanvas) {
                    return;
                }

                var overlay = document.createElement("div");
                overlay.style.cssText = "position:fixed;inset:0;z-index:1060;background:rgba(0,0,0,.72);display:flex;align-items:center;justify-content:center;padding:16px;";
                overlay.innerHTML = [
                    '<div style="background:#fff;border-radius:12px;max-width:900px;width:100%;padding:16px;box-shadow:0 20px 50px rgba(0,0,0,.25);">',
                    '<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;">',
                    '<strong>Vẽ chữ ký</strong>',
                    '<button type="button" data-psm-close style="border:0;background:transparent;font-size:24px;line-height:1;">&times;</button>',
                    "</div>",
                    '<canvas style="width:100%;height:min(60vh,420px);border:1px solid #D1D1D1;border-radius:8px;touch-action:none;background:#fff;"></canvas>',
                    '<div style="display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap;margin-top:12px;">',
                    '<button type="button" data-psm-clear class="psm-btn psm-btn--secondary">Xóa</button>',
                    '<button type="button" data-psm-save class="psm-btn psm-btn--primary">Lưu chữ ký</button>',
                    "</div>",
                    "</div>",
                ].join("");

                root.appendChild(overlay);

                var modalCanvas = overlay.querySelector("canvas");
                var rect = modalCanvas.getBoundingClientRect();
                modalCanvas.width = rect.width;
                modalCanvas.height = rect.height;
                modalCanvas.getContext("2d").drawImage(originalCanvas, 0, 0, modalCanvas.width, modalCanvas.height);
                bindDrawing(modalCanvas);

                function close() {
                    if (overlay.parentNode) {
                        overlay.parentNode.removeChild(overlay);
                    }
                }

                overlay.querySelector("[data-psm-close]").addEventListener("click", close);
                overlay.querySelector("[data-psm-clear]").addEventListener("click", function () {
                    modalCanvas.getContext("2d").clearRect(0, 0, modalCanvas.width, modalCanvas.height);
                });
                overlay.querySelector("[data-psm-save]").addEventListener("click", function () {
                    var ctx = originalCanvas.getContext("2d");
                    ctx.clearRect(0, 0, originalCanvas.width, originalCanvas.height);
                    ctx.drawImage(modalCanvas, 0, 0, originalCanvas.width, originalCanvas.height);
                    updateSignatureInput(originalCanvas);
                    close();
                });
            });
        });
    }

    function initListFilter(root) {
        each(root.querySelectorAll(".psm-list-filter"), function (input) {
            var target = input.getAttribute("data-psm-filter-target") || ".psm-table tbody tr";
            var rows = root.querySelectorAll(target);
            var clearButton = input.closest(".psm-list-filter-wrap") ?
                input.closest(".psm-list-filter-wrap").querySelector(".psm-list-filter__clear") :
                null;
            var count = root.querySelector("[data-psm-filter-count]");
            var total = rows.length;

            function renderCount(visible) {
                if (!count) {
                    return;
                }
                count.textContent = visible + " / " + total + " hồ sơ";
            }

            function applyFilter() {
                var query = input.value.trim().toLowerCase();
                var visible = 0;
                each(rows, function (row) {
                    var matches = !query || row.textContent.toLowerCase().indexOf(query) !== -1;
                    row.hidden = !matches;
                    if (matches) {
                        visible += 1;
                    }
                });
                if (clearButton) {
                    clearButton.hidden = !query;
                }
                renderCount(visible);
            }

            input.addEventListener("input", applyFilter);
            if (clearButton) {
                clearButton.addEventListener("click", function () {
                    input.value = "";
                    applyFilter();
                    input.focus();
                });
            }
            renderCount(total);
        });
    }

    function initRowClickable(root) {
        each(root.querySelectorAll(".psm-table tbody tr[data-href]"), function (row) {
            row.addEventListener("click", function (ev) {
                if (ev.target.closest("a, button, input, select, textarea, label")) {
                    return;
                }
                window.location.href = row.getAttribute("data-href");
            });

            row.addEventListener("keydown", function (ev) {
                if (ev.key !== "Enter" && ev.key !== " ") {
                    return;
                }
                if (ev.target.closest("a, button, input, select, textarea, label")) {
                    return;
                }
                ev.preventDefault();
                window.location.href = row.getAttribute("data-href");
            });
        });
    }

    ready(function () {
        each(document.querySelectorAll(ROOT_SELECTOR), function (root) {
            initAutoResizeTextareas(root);
            initFormProgress(root);
            initUnsavedGuard(root);
            initRejectConfirm(root);
            initSubmitLoading(root);
            initSignatureFullscreen(root);
            initListFilter(root);
            initRowClickable(root);
        });
    });
})();
