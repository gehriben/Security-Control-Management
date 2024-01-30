function ConstraintsView(props) {
  return (
    <div>
      <h2>Constraints</h2>
      <div id="btnCreateNewTag"><button onClick={props.onClick} class="buttons btnGreen mbutton"> + Add New Tag </button></div>
      <table id="tblAssets">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Type</th>
            <th>Values</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Impcat</td>
            <td>The impact which a breach on the asset would have.</td>
            <td>String</td>
            <td>Low, Medium, High</td>
            <td><button>Edit</button> <button>Delete</button></td>
          </tr>
          <tr>
            <td>Asset Stock</td>
            <td>TThe amount of assets which are at minimum needed in the network.</td>
            <td>Integer</td>
            <td>Min: 1</td>
            <td><button>Edit</button> <button>Delete</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default ConstraintsView;