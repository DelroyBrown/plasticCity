document.addEventListener("DOMContentLoaded", function () {
  // Set up the scene, camera, and renderer
  const scene = new THREE.Scene();
  const section = document.querySelector("#tab-es6");

  if (section) {
    const camera = new THREE.PerspectiveCamera(
      75,
      section.clientWidth / section.clientHeight,
      0.1,
      1000
    );

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(section.clientWidth, section.clientHeight);
    section.appendChild(renderer.domElement);

    // Create the cat head
    const geometry = new THREE.SphereGeometry(1, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0xff00ff });
    const catHead = new THREE.Mesh(geometry, material);
    scene.add(catHead);

    camera.position.z = 5;

    // Set up the animation loop
    function animate() {
      requestAnimationFrame(animate);

      catHead.rotation.x += 0.01;
      catHead.rotation.y += 0.01;

      renderer.render(scene, camera);
    }

    animate();
  } else {
    console.error("Section with id 'tab-es6' not found");
  }
});
