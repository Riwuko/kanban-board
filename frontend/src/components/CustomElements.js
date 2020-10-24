import * as React from "react";
import { Button, Checkbox, Text, Image, Flex } from "@chakra-ui/core";

const MarginWidest = "45px";

export const ButtonSubmit = ({ type, text }) => {
  return (
    <Button
      type={type}
      marginY={MarginWidest}
      border="none"
      backgroundColor="black"
      justifySelf="flex-start"
      color="white"
    >
      {text}
    </Button>
  );
};

export const CheckboxForm = React.forwardRef((props, ref) => (
  <Checkbox
    name={props.name}
    size={["lg", "s"]}
    variantColor={props.variantColor}
    border="grey"
    ref={ref}
  >
    {props.text}
  </Checkbox>
));

export const ImageLogo = ({ src, text, alt }) => {
  return (
    <Flex alignItems="center" marginX="20px">
      <Image src={src} alt={alt} height="50px" /> {text}
    </Flex>
  );
};

export const TextError = ({ text }) => {
  return (
    <Text color="red.500" fontSize="xs" margin="1px" padding="1px">
      {text}
    </Text>
  );
};
