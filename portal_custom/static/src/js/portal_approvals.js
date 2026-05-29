/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

function getBootstrapModalApi() {
    return window.bootstrap || (window.odoo && window.odoo.bootstrap) || null;
}

function showManualModal(modalEl) {
    modalEl.style.display = "block";
    modalEl.removeAttribute("aria-hidden");
    modalEl.setAttribute("aria-modal", "true");
    modalEl.classList.add("show");
    document.body.classList.add("modal-open");
    document.body.style.overflow = "hidden";
}

function hideManualModal(modalEl) {
    modalEl.classList.remove("show");
    modalEl.style.display = "none";
    modalEl.setAttribute("aria-hidden", "true");
    modalEl.removeAttribute("aria-modal");
    document.body.classList.remove("modal-open");
    document.body.style.overflow = "";
}

function showModal(modalId) {
    const modalEl = document.getElementById(modalId);
    const bootstrapApi = getBootstrapModalApi();
    if (modalEl && bootstrapApi && bootstrapApi.Modal) {
        const modal = bootstrapApi.Modal.getOrCreateInstance(modalEl);
        modal.show();
        return modal;
    }
    if (modalEl) {
        showManualModal(modalEl);
        return { manual: true, element: modalEl };
    }
    return null;
}

function hideModal(modalId) {
    const modalEl = document.getElementById(modalId);
    const bootstrapApi = getBootstrapModalApi();
    if (modalEl && bootstrapApi && bootstrapApi.Modal) {
        const modal = bootstrapApi.Modal.getInstance(modalEl);
        if (modal) {
            modal.hide();
        }
        return;
    }
    if (modalEl) {
        hideManualModal(modalEl);
    }
}

function callOdooRpc(url, params) {
    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            jsonrpc: "2.0",
            method: "call",
            params: params,
            id: Math.floor(Math.random() * 1000000),
        }),
    }).then((response) => response.json()).then((data) => {
        if (data.error) {
            throw new Error(data.error.data?.message || data.error.message || "Unknown error");
        }
        return data.result;
    });
}

function showAlert(type, message) {
    const alertHtml = '<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' +
        message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
        "</div>";
    $(".container").first().prepend(alertHtml);
    setTimeout(function () {
        $(".alert").fadeOut();
    }, 3000);
}

function removeRequestRow(requestId) {
    const $row = $('.request-row[data-request-id="' + requestId + '"]');
    $row.fadeOut(300, function () {
        $(this).remove();
    });
}

publicWidget.registry.PortalApproveShift = publicWidget.Widget.extend({
    selector: ".js_approve_shift",
    events: {
        click: "_onClick",
    },

    _onClick(ev) {
        ev.preventDefault();
        const $btn = $(ev.currentTarget);
        const slotId = $btn.data("slot-id");

        if (!slotId) {
            alert("Loi: Khong tim thay ID ca lam viec.");
            return;
        }

        if (!confirm("Ban co chac muon duyet ca lam viec nay?")) {
            return;
        }

        $btn.prop("disabled", true);
        $btn.html('<i class="fa fa-spinner fa-spin"></i>');

        callOdooRpc("/my/approvals/approve-shift", { slot_id: slotId })
            .then((result) => {
                if (result.success) {
                    const $row = $btn.closest("tr, .shift-row");
                    $row.fadeOut(300, function () {
                        $(this).remove();
                        showAlert("success", result.message || "Da duyet thanh cong!");
                    });
                } else {
                    alert(result.error || "Co loi xay ra.");
                    $btn.prop("disabled", false);
                    $btn.html('<i class="fa fa-check"></i> Duyet');
                }
            })
            .catch((err) => {
                alert("Loi: " + err.message);
                $btn.prop("disabled", false);
                $btn.html('<i class="fa fa-check"></i> Duyet');
            });
    },
});

publicWidget.registry.PortalRejectShift = publicWidget.Widget.extend({
    selector: ".js_reject_shift",
    events: {
        click: "_onClick",
    },

    _onClick(ev) {
        ev.preventDefault();
        const $btn = $(ev.currentTarget);
        const slotId = $btn.data("slot-id");

        if (!slotId) {
            alert("Loi: Khong tim thay ID ca lam viec.");
            return;
        }

        const reason = prompt("Nhap ly do tu choi (tuy chon):");
        if (reason === null) {
            return;
        }

        $btn.prop("disabled", true);
        $btn.html('<i class="fa fa-spinner fa-spin"></i>');

        callOdooRpc("/my/approvals/reject-shift", { slot_id: slotId, reason: reason })
            .then((result) => {
                if (result.success) {
                    const $row = $btn.closest("tr, .shift-row");
                    $row.fadeOut(300, function () {
                        $(this).remove();
                        showAlert("warning", result.message || "Da tu choi ca.");
                    });
                } else {
                    alert(result.error || "Co loi xay ra.");
                    $btn.prop("disabled", false);
                    $btn.html('<i class="fa fa-times"></i> Tu choi');
                }
            })
            .catch((err) => {
                alert("Loi: " + err.message);
                $btn.prop("disabled", false);
                $btn.html('<i class="fa fa-times"></i> Tu choi');
            });
    },
});

publicWidget.registry.PortalApproveRequest = publicWidget.Widget.extend({
    selector: ".js_approve_request",
    events: {
        click: "_onClick",
    },

    _onClick(ev) {
        ev.preventDefault();
        const $btn = $(ev.currentTarget);
        const requestId = $btn.data("request-id");
        const requestTitle = $btn.data("request-title") || "Yeu cau phe duyet";

        if (!requestId) {
            alert("Loi: Khong tim thay ID yeu cau.");
            return;
        }

        $("#modal_request_approve_id").val(requestId);
        $("#modal_request_approve_title").text(requestTitle);

        if (!showModal("requestApproveModal")) {
            if (confirm('Ban co chac muon duyet "' + requestTitle + '"?')) {
                $("#btn_confirm_request_approve").trigger("click");
            }
        }
    },
});

publicWidget.registry.PortalRejectRequest = publicWidget.Widget.extend({
    selector: ".js_reject_request",
    events: {
        click: "_onClick",
    },

    _onClick(ev) {
        ev.preventDefault();
        const $btn = $(ev.currentTarget);
        const requestId = $btn.data("request-id");
        const requestTitle = $btn.data("request-title") || "Yeu cau phe duyet";

        if (!requestId) {
            alert("Loi: Khong tim thay ID yeu cau.");
            return;
        }

        $("#modal_request_reject_id").val(requestId);
        $("#modal_request_reject_title").text(requestTitle);
        $("#modal_request_reject_reason").val("");

        if (!showModal("requestRejectModal")) {
            const fallbackReason = prompt('Nhap ly do tu choi cho "' + requestTitle + '" (tuy chon):', "");
            if (fallbackReason === null) {
                return;
            }
            $("#modal_request_reject_reason").val(fallbackReason);
            $("#btn_confirm_request_reject").trigger("click");
        }
    },
});

publicWidget.registry.PortalOpenFinalResignationAction = publicWidget.Widget.extend({
    selector: ".js_open_final_resignation_action",
    events: {
        click: "_onClick",
    },

    _onClick(ev) {
        ev.preventDefault();
        const $btn = $(ev.currentTarget);
        const requestId = $btn.data("request-id");
        const requestTitle = $btn.data("request-title") || "Don nghi viec";
        const actionCode = $btn.data("action-code");
        const modalTitle = $btn.data("modal-title") || "Xu ly buoc cuoi";
        const modalNote = $btn.data("modal-note") || "";
        const modalClass = $btn.data("modal-class") || "success";

        if (!requestId || !actionCode) {
            alert("Loi: Khong tim thay thong tin hanh dong.");
            return;
        }

        $("#modal_resignation_final_request_id").val(requestId);
        $("#modal_resignation_final_action_code").val(actionCode);
        $("#modal_resignation_final_request_title").text(requestTitle);
        $("#modal_resignation_final_title").text(modalTitle);
        $("#modal_resignation_final_note").text(modalNote);

        const $header = $("#modal_resignation_final_header");
        const $highlight = $("#modal_resignation_final_highlight");
        $header.removeClass("bg-success bg-danger bg-warning text-dark text-white");
        $highlight.removeClass("modal-highlight-success modal-highlight-danger");

        if (modalClass === "warning") {
            $header.addClass("bg-warning text-dark");
            $highlight.addClass("modal-highlight-success");
        } else if (modalClass === "danger") {
            $header.addClass("bg-danger text-white");
            $highlight.addClass("modal-highlight-danger");
        } else {
            $header.addClass("bg-success text-white");
            $highlight.addClass("modal-highlight-success");
        }

        if (!showModal("resignationFinalActionModal")) {
            if (confirm(modalTitle + ': "' + requestTitle + '"?')) {
                $("#btn_confirm_resignation_final_action").trigger("click");
            }
        }
    },
});

publicWidget.registry.PortalApproveLeave = publicWidget.Widget.extend({
    selector: ".js_approve_leave",
    events: {
        click: "_onClick",
    },

    _onClick(ev) {
        ev.preventDefault();
        const $btn = $(ev.currentTarget);
        const leaveId = $btn.data("leave-id");
        const employeeName = $btn.data("employee-name");
        const leaveInfo = $btn.data("leave-info");

        if (!leaveId) {
            alert("Loi: Khong tim thay ID don nghi.");
            return;
        }

        $("#modal_leave_id").val(leaveId);
        $("#modal_employee_name").text(employeeName);
        $("#modal_leave_info").text(leaveInfo);

        const $select = $("#replacement_employee_id");
        $select.html('<option value="">-- Dang tai danh sach... --</option>');
        $select.prop("disabled", true);

        if (showModal("leaveApprovalModal")) {
            callOdooRpc("/my/approvals/leave-replacement-candidates", { leave_id: leaveId })
                .then((result) => {
                    let html = '<option value="">-- Khong co nguoi thay the --</option>';
                    if (result.candidates && result.candidates.length > 0) {
                        result.candidates.forEach((candidate) => {
                            html += '<option value="' + candidate.id + '">' + candidate.name + " (" + candidate.dept + ")</option>";
                        });
                    }
                    $select.html(html);
                    $select.prop("disabled", false);
                })
                .catch(() => {
                    $select.html('<option value="">-- Loi khi tai danh sach --</option>');
                });
        }
    },
});

$(document).on("click", "#btn_confirm_request_approve", function () {
    const requestId = $("#modal_request_approve_id").val();
    const $btn = $(this);
    const originalHtml = $btn.html();

    if (!requestId) {
        alert("Loi: Khong tim thay ID yeu cau.");
        return;
    }

    $btn.prop("disabled", true);
    $btn.html('<i class="fa fa-spinner fa-spin me-1"></i>Dang duyet...');

    callOdooRpc("/my/approvals/approve-request", { request_id: requestId })
        .then((result) => {
            if (result.success) {
                hideModal("requestApproveModal");
                removeRequestRow(requestId);
                showAlert("success", result.message || "Da duyet thanh cong!");
            } else {
                alert(result.error || "Co loi xay ra.");
            }
        })
        .catch((err) => {
            alert("Loi: " + err.message);
        })
        .finally(() => {
            $btn.prop("disabled", false);
            $btn.html(originalHtml);
        });
});

$(document).on("click", "#btn_confirm_request_reject", function () {
    const requestId = $("#modal_request_reject_id").val();
    const reason = $("#modal_request_reject_reason").val();
    const $btn = $(this);
    const originalHtml = $btn.html();

    if (!requestId) {
        alert("Loi: Khong tim thay ID yeu cau.");
        return;
    }

    $btn.prop("disabled", true);
    $btn.html('<i class="fa fa-spinner fa-spin me-1"></i>Dang tu choi...');

    callOdooRpc("/my/approvals/reject-request", { request_id: requestId, reason: reason })
        .then((result) => {
            if (result.success) {
                hideModal("requestRejectModal");
                removeRequestRow(requestId);
                showAlert("warning", result.message || "Da tu choi yeu cau.");
            } else {
                alert(result.error || "Co loi xay ra.");
            }
        })
        .catch((err) => {
            alert("Loi: " + err.message);
        })
        .finally(() => {
            $btn.prop("disabled", false);
            $btn.html(originalHtml);
        });
});

$(document).on("click", "#btn_confirm_resignation_final_action", function () {
    const requestId = $("#modal_resignation_final_request_id").val();
    const actionCode = $("#modal_resignation_final_action_code").val();
    const $btn = $(this);
    const originalHtml = $btn.html();

    if (!requestId || !actionCode) {
        alert("Loi: Khong tim thay thong tin hanh dong.");
        return;
    }

    $btn.prop("disabled", true);
    $btn.html('<i class="fa fa-spinner fa-spin me-1"></i>Dang xu ly...');

    callOdooRpc("/my/approvals/finalize-resignation", {
        request_id: requestId,
        action_code: actionCode,
    })
        .then((result) => {
            if (result.success) {
                hideModal("resignationFinalActionModal");
                window.location.href = result.redirect_url || "/my/approvals";
            } else {
                alert(result.error || "Co loi xay ra.");
            }
        })
        .catch((err) => {
            alert("Loi: " + err.message);
        })
        .finally(() => {
            $btn.prop("disabled", false);
            $btn.html(originalHtml);
        });
});

$(document).on("click", "#btn_confirm_leave_approval", function () {
    const leaveId = $("#modal_leave_id").val();
    const replacementId = $("#replacement_employee_id").val();
    const $btn = $(this);
    const originalHtml = $btn.html();

    $btn.prop("disabled", true);
    $btn.html('<i class="fa fa-spinner fa-spin me-1"></i>Dang duyet...');

    callOdooRpc("/my/team/leave/approve", {
        leave_id: leaveId,
        replacement_employee_id: replacementId || null,
    }).then((result) => {
        if (result.success) {
            hideModal("leaveApprovalModal");

            const $row = $('.leave-row[data-leave-id="' + leaveId + '"]');
            $row.fadeOut(300, function () {
                $(this).remove();
            });
        } else {
            alert(result.error || "Co loi xay ra.");
        }
    }).catch((err) => {
        alert("Loi: " + err.message);
    }).finally(() => {
        $btn.prop("disabled", false);
        $btn.html(originalHtml);
    });
});

$(document).on("click", '[data-bs-dismiss="modal"]', function () {
    const modalEl = this.closest(".modal");
    if (modalEl && !getBootstrapModalApi()) {
        hideManualModal(modalEl);
    }
});

$(document).on("click", ".modal", function (ev) {
    if (ev.target === ev.currentTarget && !getBootstrapModalApi()) {
        hideManualModal(ev.currentTarget);
    }
});

publicWidget.registry.PortalRejectLeave = publicWidget.Widget.extend({
    selector: ".js_reject_leave",
    events: {
        click: "_onClick",
    },

    _onClick(ev) {
        ev.preventDefault();
        const $btn = $(ev.currentTarget);
        const leaveId = $btn.data("leave-id");

        if (!leaveId) {
            alert("Loi: Khong tim thay ID don nghi.");
            return;
        }

        const reason = prompt("Nhap ly do tu choi don nghi phep:");
        if (reason === null) {
            return;
        }

        $btn.prop("disabled", true);
        $btn.html('<i class="fa fa-spinner fa-spin"></i>');

        callOdooRpc("/my/team/leave/reject", { leave_id: leaveId, reason: reason })
            .then((result) => {
                if (result.success) {
                    const $row = $btn.closest(".leave-row");
                    $row.fadeOut(300, function () {
                        $(this).remove();
                    });
                } else {
                    alert(result.error || "Co loi xay ra.");
                    $btn.prop("disabled", false);
                    $btn.html('<i class="fa fa-times"></i> Tu choi');
                }
            })
            .catch((err) => {
                alert("Loi: " + err.message);
                $btn.prop("disabled", false);
                $btn.html('<i class="fa fa-times"></i> Tu choi');
            });
    },
});

export default {
    PortalApproveShift: publicWidget.registry.PortalApproveShift,
    PortalRejectShift: publicWidget.registry.PortalRejectShift,
    PortalApproveRequest: publicWidget.registry.PortalApproveRequest,
    PortalRejectRequest: publicWidget.registry.PortalRejectRequest,
    PortalApproveLeave: publicWidget.registry.PortalApproveLeave,
    PortalRejectLeave: publicWidget.registry.PortalRejectLeave,
};
