#!/usr/bin/env python
"""
Performs basic cleaning on the data and sve the results in Weights $ Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
    local_path = wandb.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)

    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    # Drop rows not in proper geolocation
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Save result
    df.to_csv("clean_sample.csv", index=False)

    # Save postprocessed data W&B
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file('clean_sample.csv')
    run.log_artifact(artifact)

    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="input artifact to basic_cleaning",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="output artifact of basic_cleaning",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="description of the output artifact generated",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="the type of the output artifact",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,  ## INSERT TYPE HERE: str, float or int,
        help="minimum price to consider in basic_cleaning",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,  ## INSERT TYPE HERE: str, float or int,
        help="maximum price to consider in basic_cleaning",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    args = parser.parse_args()

    go(args)
