import React from "react";
import { Nav, NavLink, Bars, NavMenu } from "./NavbarElements";
import Logo from "./logo.png";
import "./nav.css";

const Navbar = () => {
  return (
    <>
      <Nav>
        <NavLink to="/">
          <img src={Logo} alt="logo" style={{ height: 50 }} />
        </NavLink>
        <Bars />

        <NavMenu>
          <NavLink to="/home" activeStyle>
            Home
          </NavLink>
          <div class="dropdown">
            <button class="dropdown">About</button>
            <div class="dropdown-content">
              <NavLink to="/aboutgid" activeStyle>
                About GID
              </NavLink>
              <NavLink to="/aboutus" activeStyle>
                About Us
              </NavLink>
            </div>
          </div>
          <NavLink to="/begin" activeStyle>
            File(s) Analysis
          </NavLink>
          <NavLink to="/onlineAnalysis" activeStyle>
            Live Analysis
          </NavLink>
          <NavLink to="/howto" activeStyle>
            How To
          </NavLink>
        </NavMenu>
      </Nav>
    </>
  );
};

export default Navbar;
