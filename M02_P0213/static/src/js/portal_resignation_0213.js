(function () {
    "use strict";

    var root = document.querySelector(".o_psm_0213_portal");
    if (!root) {
        return;
    }

    var scrollTopButton = root.querySelector(".psm-scroll-top");
    var progressLinks = Array.prototype.slice.call(root.querySelectorAll(".psm-form-progress__dot"));
    var sections = progressLinks
        .map(function (link) {
            var targetId = link.getAttribute("href");
            if (!targetId || targetId.charAt(0) !== "#") {
                return null;
            }
            return root.querySelector(targetId);
        })
        .filter(Boolean);

    if (scrollTopButton) {
        function syncScrollTopButton() {
            scrollTopButton.classList.toggle("is-visible", window.scrollY > 240);
        }

        scrollTopButton.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth",
            });

            if (window.history && window.history.replaceState) {
                window.history.replaceState(null, "", window.location.pathname + window.location.search);
            }
        });

        window.addEventListener("scroll", syncScrollTopButton, { passive: true });
        syncScrollTopButton();
    }

    if (!progressLinks.length || !sections.length) {
        return;
    }

    function setActive(targetId) {
        progressLinks.forEach(function (link) {
            var isActive = link.getAttribute("href") === "#" + targetId;
            link.classList.toggle("is-active", isActive);
            if (isActive) {
                link.setAttribute("aria-current", "step");
            } else {
                link.removeAttribute("aria-current");
            }
        });
    }

    progressLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            var targetId = link.getAttribute("href");
            var target = targetId && root.querySelector(targetId);
            if (!target) {
                return;
            }

            event.preventDefault();
            target.scrollIntoView({
                behavior: "smooth",
                block: "start",
            });
            setActive(target.id);

            if (window.history && window.history.replaceState) {
                window.history.replaceState(null, "", targetId);
            }
        });
    });

    if ("IntersectionObserver" in window) {
        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        setActive(entry.target.id);
                    }
                });
            },
            {
                root: null,
                rootMargin: "-25% 0px -60% 0px",
                threshold: 0.01,
            }
        );

        sections.forEach(function (section) {
            observer.observe(section);
        });
    }
})();
