import React from "react";
import { Flex, Image } from "@chakra-ui/core";
import SignUpPage from "./SignUpForm";
import background from "../styles/img/border.jpeg";

const Registration = () => {
  return (
    <Flex justifyContent="center" alignItems="center" minHeight="100vh">
      <Flex
        height={["90vh", "90vh", "90vh", "70vh"]}
        width={["100vw", "100vw", "100vw", "80vw", "30vw"]}
        backgroundColor="white"
        borderRadius={["20px", "20px", "20px", "20", "20px 0px 0px 20px"]}
      >
        <SignUpPage />
      </Flex>
      <Flex height="70vh" display={["none", "none", "none", "none", "flex"]}>
        <Image
          src={background}
          borderRadius={"0px 20px 20px 0px"}
          objectFit="cover"
        />
      </Flex>
    </Flex>
  );
};

export default Registration;
