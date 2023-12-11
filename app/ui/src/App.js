// import logo from './logo.svg';
import './App.css';

const products = [
  { id: 10, name: "Apple", price: 350.0 },
  { id: 14, name: "Orange", price: 200.0 },
  { id: 12, name: "grapes", price: 150.0 },
  { id: 16, name: "potato", price: 15.0 },
  { id: 21, name: "onion", price: 30.0 },
];

function NewComp2() {
  const items = products.map((product) => (
    <li key={product.id}>{product.name}</li>
  ));

  return (
    <>
      <ul>{items}</ul>
    </>
  );
}

function NewBtn1(){

  function handleClick1(){
      alert("This is event alert");
  }

  return (
    <>
      <button onClick={handleClick1}>
        Change
      </button>
    </>
  );
}

function NewComp1(){
  return (
    <>
      <div id="test1">Hello World!</div>
    </>
  );
}

function App() {
  return (
    <>
      <NewComp1 />
      <NewBtn1 />
      <NewComp2 />
    </>
  );
}

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

export default App;
